# gradio_app.py
import gradio as gr
import os, sys, time, traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.chat_bot import Chatbot

# Khởi tạo chatbot
chatbot_instance = None
try:
    print("🚀 Đang khởi tạo AniBot...")
    chatbot_instance = Chatbot(config_path='config/config.yaml', model_config_path='config/model_config.json')
    print("✨ AniBot đã sẵn sàng!")
except Exception as e:
    print(f"❌ LỖI NGHIÊM TRỌNG KHI KHỞI TẠO: {e}")
    traceback.print_exc()

def user(user_message, history):
    return "", history + [[user_message, None]]

def bot(history):
    if not chatbot_instance:
        history[-1][1] = "❌ Lỗi: Chatbot chưa được khởi tạo thành công."
        yield history
        return
    
    user_message = history[-1][0]
    try:
        response = chatbot_instance.answer(user_message, history[:-1])
        history[-1][1] = ""
        for char in response:
            history[-1][1] += char
            time.sleep(0.005)
            yield history
    except Exception as e:
        history[-1][1] = "😔 Xin lỗi, đã có lỗi hệ thống xảy ra."
        yield history

# Giao diện
with gr.Blocks(theme=gr.themes.Soft(primary_hue="orange")) as demo:
    gr.HTML("<h1>🎌 AniBot - Chuyên gia Anime & Manga</h1>")
    chatbot = gr.Chatbot(label="Trò chuyện", height=600)
    with gr.Row():
        msg = gr.Textbox(placeholder="Hỏi tôi bất cứ điều gì về anime...", scale=4, show_label=False)
        submit_btn = gr.Button("🚀 Gửi", variant="primary", scale=1)
    
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    submit_btn.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)

if __name__ == "__main__":
    print("\n🌐 Đang khởi động Gradio interface...")
    demo.queue().launch(share=True, server_name="0.0.0.0", server_port=7861)