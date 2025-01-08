import gradio as gr
from transformers import AutoModel, AutoTokenizer

from vector_search import search

print("正在加载模型")

# 加载模型和分词器
tokenizer = AutoTokenizer.from_pretrained(
    "SDUIRLab/fuzi-mingcha-v1_0", trust_remote_code=True
)
model = AutoModel.from_pretrained(
    "SDUIRLab/fuzi-mingcha-v1_0", trust_remote_code=True, device_map="auto"
).half()
model = model.eval()

print("模型加载完毕")

# 全局变量
history = []


def process_lucence_input(input_text):
    nr = ["(", ")", "[", "]", "{", "}", "/", "?", "!", "^", "*", "-", "+"]
    for char in nr:
        input_text = input_text.replace(char, f"\\{char}")
    return input_text


def chat(prompt, history=None):
    if history is None:
        history = []
    response, history = model.chat(
        tokenizer,
        prompt,
        history=history if history else [],
        max_length=4096,
        max_time=100,
        top_p=0.7,
        temperature=0.95,
    )
    return response, history


def handle_request(task, user_input):
    global history
    response = ""
    if task == "法条检索回复":
        # Task 1: 法条检索
        prompt1_task1 = f"请根据以下问题生成相关法律法规: {user_input}"
        print(f"【法条检索任务】用户输入内容 ----> {user_input}")
        generate_law, _ = chat(prompt1_task1)
        print(f"大模型根据用户问题生成的，供下步进行检索的法律法规：\n\t{generate_law}")
        try:
            docs = search("fatiao", generate_law, 3)
            print(f"法条检索响应内容 ----> {docs}")
            retrieval_law = "\n".join(
                [f"第{i+1}条：\n{doc}" for i, doc in enumerate(docs)]
            )
        except Exception as e:
            print(f"进行法条检索时发生错误 ----> {e}")
            retrieval_law = ""
        prompt2_task1 = f"请根据下面相关法条回答问题\n相关法条：\n{retrieval_law}\n问题：\n{user_input}"
        response, _ = chat(prompt2_task1)
    elif task == "案例检索回复":
        # Task 2: 类案检索
        prompt1_task2 = f"请根据以下问题生成相关案例: {user_input}"
        print(f"【案例检索任务】用户输入内容 ----> {user_input}")
        generate_case, _ = chat(prompt1_task2)
        print(f"大模型根据用户问题生成的，供下步进行检索的案例：\n\t{generate_case}")
        try:
            docs = search("anli", generate_case, 1)
            print(f"案例检索返回内容 ----> {docs}")
            max_len = 1000
            retrieval_case = "\n".join(
                [
                    f"第{i+1}条：\n{doc[int(-max_len / len(docs)):]}"
                    for i, doc in enumerate(docs)
                ]
            )
        except Exception as e:
            print(f"进行案例检索时发生错误 ----> {e}")
            retrieval_case = ""
        prompt2_task2 = f"请根据下面相关案例回答问题\n相关案例：\n{retrieval_case}\n问题：\n{user_input}"
        response, _ = chat(prompt2_task2)
    elif task == "三段论推理判决":
        # Task 3: 三段论推理
        prompt_task3 = f"请根据基本案情，利用三段论的推理方式得到判决结果，判决结果包括：1.罪名；2.刑期。\n基本案情：{user_input}"
        print(f"【三段论推理任务】用户输入内容 ----> {user_input}")
        response, _ = chat(prompt_task3)
    elif task == "司法对话":
        # Task 4: 司法对话
        print(f"【司法对话任务】用户输入内容 ----> {user_input}")
        response, history = chat(user_input, history)
    return response


# 创建 Gradio 界面
task_options = ["法条检索回复", "案例检索回复", "三段论推理判决", "司法对话"]
task_placeholders = {
    "法条检索回复": "欢迎使用 基于法条检索回复 任务，此任务中模型首先根据用户输入案情，模型生成相关法条；根据生成的相关法条检索真实法条；最后结合真实法条回答用户问题。您可以尝试输入以下内容：\n\n\n小李想开办一家个人独资企业，他需要准备哪些信息去进行登记注册？",
    "案例检索回复": "欢迎使用 基于案例检索回复 任务，此任务中模型首先根据用户输入案情，模型生成相关案例；根据生成的相关案例检索真实案例；最后结合真实案例回答用户问题。您可以尝试输入以下内容：\n\n\n被告人夏某在2007年至2010年期间，使用招商银行和广发银行的信用卡在北京纸老虎文化交流有限公司等地透支消费和取现。尽管经过银行多次催收，夏某仍欠下两家银行共计人民币26379.85元的本金。2011年3月15日，夏某因此被抓获，并在到案后坦白了自己的行为。目前，涉案的欠款已被还清。请问根据上述事实，该如何判罚夏某？",
    "三段论推理判决": "欢迎使用 三段论推理判决 任务，此任务中模型利用三段论的推理方式生成判决结果。您可以尝试输入以下内容：\n\n\n被告人陈某伙同王某（已判刑）在邵东县界岭乡峰山村艾窑小学法经营“地下六合彩”，由陈某负责联系上家，王某1负责接单卖码及接受投注，并约定将收受投注10％的提成按三七分成，陈某占三，王某1占七。该地下六合彩利用香港“六合彩”开奖结果作为中奖号码，买1到49中间的一个或几个数字，赔率为1：42。在香港六合彩开奖的当天晚上点三十分前，停止卖号，将当期购买的清单报给姓赵的上家。开奖后从网上下载香港六合彩的中奖号码进行结算赔付，计算当天的中奖数额，将当期卖出的总收入的百分之十留给自己，用总收入的百分之九十减去中奖的钱，剩余的为付给上家的钱。期间，二人共同经营“地下六合彩”40余期，收受吕某、吕永玉、王某2、王某3等人的投注额约25万余元，两人共计非法获利4万余元。被告人陈某于2013年11月18日被抓获，后被取保候审，在取保期间，被告人陈某脱逃。2015年1月21公安机关对其网上追逃。2017年6月21日被告人陈某某自动到公安机关投案。上述事实，被告人陈某在开庭审理过程中亦无异议，并有证人王某1、吕某、吕永玉、王某3等人的证言，扣押决定书，扣押物品清单，文件清单，抓获经过，刑事判决书，户籍证明等证据证实，足以认定。",
    "司法对话": "欢迎使用 司法对话 任务，此任务中您可以与模型进行直接对话。",
}

with gr.Blocks() as demo:
    gr.Markdown("## 夫子·明察 司法大模型 Web 服务")

    # 顶部任务选择
    with gr.Row():
        task = gr.Dropdown(
            label="选择任务", choices=task_options, value=task_options[0]
        )

    # 下方 "用户输入" 和 "模型回复" 并列
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(
                label="用户输入",
                placeholder=task_placeholders[task_options[0]],
                lines=16,
            )
        with gr.Column():
            output = gr.Textbox(label="模型回复", lines=16)

    # 提交按钮放置在下方中央
    with gr.Row():
        submit_button = gr.Button("提交", elem_id="submit_button")

    # 动态更新 Placeholder
    def update_placeholder(selected_task):
        return task_placeholders[selected_task]

    task.change(
        fn=update_placeholder, inputs=[task], outputs=[user_input], show_progress=False
    )

    # 绑定按钮点击事件
    submit_button.click(handle_request, inputs=[task, user_input], outputs=output)

# 启动 Gradio 服务
demo.launch(server_name="0.0.0.0")
