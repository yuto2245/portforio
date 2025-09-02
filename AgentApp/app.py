import os
import chainlit as cl
from chainlit.input_widget import Select

# --- Provider SDKs ---
from openai import OpenAI
from anthropic import AsyncAnthropic
from groq import AsyncGroq
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch, UrlContext

# --- Langchain Core ---
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --- Environment Loading ---
from dotenv import load_dotenv
load_dotenv()

# ---日付の取得 ---
from datetime import datetime
now = datetime.now()
print("日付と時刻",now)

# --- APIキーの読み込みとクライアントの初期化 ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

# クライアントはグローバルに初期化しておくと効率的
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
anthropic_client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None
grok_client = AsyncGroq(api_key=XAI_API_KEY) if XAI_API_KEY else None
gemini_client = genai.Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None

# Chainlitのトレース機能
cl.instrument_openai()

# --- モデルリストの定義 ---
AVAILABLE_MODELS = [
    { "label": "GPT-4o-mini", "value": "gpt-4o-mini", "type": "openai" },
    { "label": "GPT-4.1", "value": "gpt-4.1-2025-04-14", "type": "openai" },
    { "label": "GPT-5 Chat", "value": "gpt-5-chat-latest", "type": "openai" },
    { "label": "GPT-5 Nano", "value": "gpt-5-nano-2025-08-07", "type": "openai" },
    { "label": "GPT-5", "value": "gpt-5-2025-08-07", "type": "openai" },
    { "label": "Gemini 2.5 Flash-Lite", "value": "gemini-2.5-flash-lite", "type": "gemini" },
    { "label": "Gemini 2.5 Flash", "value": "gemini-2.5-flash", "type": "gemini" },
    { "label": "Gemini 2.5 Pro", "value": "gemini-2.5-pro", "type": "gemini" },
    { "label": "Claude Sonnet 3.7", "value": "claude-3-7-sonnet-20250219", "type": "claude" },
    { "label": "Claude Sonnet4", "value": "claude-sonnet-4-20250514", "type": "claude" },
    { "label": "Claude Opus4.1", "value": "claude-opus-4-1-202508054", "type": "claude" },
    { "label": "Grok4", "value": "grok-4-0709", "type": "grok" },
    { "label": "Grok Code Fast 1", "value": "grok-code-fast-1", "type": "grok" },
]
DEFAULT_MODEL_INDEX = 0

# --- システムプロンプトの定義 ---
current_time = now.strftime("%Y-%m-%d %H:%M")
SYSTEM_PROMPT_CHOICES = [
    { "label": "標準アシスタント", "content": "Current time: {current_time}\nYou are a helpful assistant." },
    { "label": "丁寧な説明", "content": "Current time: {current_time}\nUse a formal tone, providing clear, well-structured sentences and precise language." },
    { "label": "簡潔な回答", "content": "Current time: {current_time}\nRespond briefly and directly, using as few words as possible." },
    { "label": "ソクラテス式", "content": "Current time: {current_time}\nRespond as a Socratic teacher, guiding the user through questions and reasoning to foster deep understanding." },
]
DEFAULT_PROMPT_INDEX = 0

# --- Chainlit App Logic ---

@cl.on_chat_start
async def start_chat():
    """チャット開始時に呼び出され、設定UIを初期化します。"""
    settings = await cl.ChatSettings([
        Select(id="model", label="モデル", values=[m["label"] for m in AVAILABLE_MODELS], initial_index=DEFAULT_MODEL_INDEX),
        Select(id="system_prompt", label="システムプロンプト（AIの性格・役割）", values=[p["label"] for p in SYSTEM_PROMPT_CHOICES], initial_index=DEFAULT_PROMPT_INDEX),
    ]).send()
    
    # 初期設定を設定
    initial_model = AVAILABLE_MODELS[DEFAULT_MODEL_INDEX]
    initial_prompt = SYSTEM_PROMPT_CHOICES[DEFAULT_PROMPT_INDEX]["content"]
    
    cl.user_session.set("model", initial_model)
    cl.user_session.set("system_prompt", initial_prompt)
    cl.user_session.set("conversation_history", [])
    
    print(f"Initial setup: Model={initial_model['label']}, Prompt={SYSTEM_PROMPT_CHOICES[DEFAULT_PROMPT_INDEX]['label']}")
    
    # 修正点① await を追加
    await setup_agent(settings)

@cl.on_settings_update
async def setup_agent(settings: dict):
    """設定が更新されたときに呼び出されます。"""
    model_label = settings["model"]
    selected_model = next((m for m in AVAILABLE_MODELS if m["label"] == model_label), AVAILABLE_MODELS[DEFAULT_MODEL_INDEX])
    cl.user_session.set("model", selected_model)

    prompt_label = settings["system_prompt"]
    selected_prompt = next((p["content"] for p in SYSTEM_PROMPT_CHOICES if p["label"] == prompt_label), SYSTEM_PROMPT_CHOICES[DEFAULT_PROMPT_INDEX]["content"])
    cl.user_session.set("system_prompt", selected_prompt)
    print(f"Settings updated: Model={selected_model['label']}, Prompt={prompt_label}")

@cl.on_message
async def on_message(message: cl.Message):
    """ユーザーからのメッセージ受信時に呼び出されます。"""
    model_info = cl.user_session.get("model")
    system_prompt = cl.user_session.get("system_prompt")
    conversation_history = cl.user_session.get("conversation_history", [])
    
    # 修正点③ None防御
    if model_info is None:
        model_info = AVAILABLE_MODELS[DEFAULT_MODEL_INDEX]
        cl.user_session.set("model", model_info)
        print(f"Model info was None, set to default: {model_info}")
    
    if system_prompt is None:
        system_prompt = SYSTEM_PROMPT_CHOICES[DEFAULT_PROMPT_INDEX]["content"]
        cl.user_session.set("system_prompt", system_prompt)
        print(f"System prompt was None, set to default")
    
    # 履歴に今回のユーザーメッセージを追加
    conversation_history.append(HumanMessage(content=message.content))
    
    # APIに渡すメッセージリストを作成
    api_messages = [msg for msg in conversation_history if not isinstance(msg, SystemMessage)]
    
    msg = cl.Message(content="")
    await msg.send()
    answer_text = ""

    try:
        # --- OpenAI Models ---
        if model_info["type"] == "openai":
            if not openai_client:
                answer_text = "エラー: OPENAI_API_KEYが設定されていません。"
                await msg.stream_token(answer_text)
                await msg.update()
                return
            
            model = model_info["value"]
            previous_response_id = cl.user_session.get("previous_response_id")

            tools = [
                {"type": "web_search"},
                {"type": "code_interpreter", "container": {"type": "auto"}},
                {"type": "image_generation"},
                {
                    "type": "mcp",
                    "server_label": "deepwiki",
                    "server_url": "https://mcp.deepwiki.com/mcp",
                    "require_approval": "never",
                }
            ] 
            response = openai_client.responses.create(
                model=model,
                input=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": message.content
                    }
                ],
                previous_response_id=previous_response_id,
                tools=tools,
                stream=True,
            ) 
            for event in response:
                etype = getattr(event, "type", None)

                # テキストトークン（増分）
                if etype == "response.output_text.delta":
                    token = getattr(event, "delta", "") or ""
                    if token:
                        answer_text += token
                        await msg.stream_token(token)

                # 出力テキスト完了（区切りイベント）
                elif etype == "response.output_text.done":
                    # ここでは特に何もしない（必要ならログ）
                    pass

                # 応答全体が完成
                elif etype == "response.completed":
                    resp = getattr(event, "response", None)
                    if resp and getattr(resp, "id", None):
                        cl.user_session.set("previous_response_id", resp.id)

                # エラーイベント
                elif etype == "response.error":
                    err = getattr(event, "error", None)
                    raise RuntimeError(str(err) if err else "OpenAI streaming error")

                # 作成開始イベントなどは無視してOK
                else:
                    # print("DEBUG OpenAI event:", event)
                    pass
        
            #正常終了後、会話履歴を更新
            if answer_text:
                conversation_history.append(AIMessage(content=answer_text))
                cl.user_session.set("conversation_history", conversation_history)
            await msg.update()

        # --- Gemini Models ---
        elif model_info["type"] == "gemini":
            if not GOOGLE_API_KEY:
                answer_text = "エラー: GOOGLE_API_KEYが設定されていません。"
                await msg.stream_token(answer_text)
                await msg.update()
                return
                
            # --- ツール設定 ---
            tools = [
                {"url_context": {}},
                {"google_search": {}},
                {"code_execution": {}},
            ]

            # システムプロンプトとメッセージを結合
            messages = [f"System: {system_prompt}"] if system_prompt else []
            messages.extend([m.content for m in api_messages])
            prompt = "\n".join(messages)

            # --- API呼び出し ---
            stream = gemini_client.models.generate_content(
                model=model_info["value"],
                contents=prompt,
                config=GenerateContentConfig(
                    tools=tools,
                )
            )

            # --- レスポンスを処理（Gemini） ---
            if hasattr(stream, "candidates") and stream.candidates:
                candidate = stream.candidates[0]  # 最上位候補のみ採用
                if getattr(candidate, "content", None):
                    for part in (candidate.content.parts or []):
                        text = getattr(part, "text", None)
                        if text:
                            answer_text += text
                            await msg.stream_token(text)

            # 会話履歴を更新
            if answer_text:
                conversation_history.append(AIMessage(content=answer_text))
                cl.user_session.set("conversation_history", conversation_history)
            await msg.update()

        # --- Claude Models ---
        elif model_info["type"] == "claude":
            if not anthropic_client:
                answer_text = "エラー: ANTHROPIC_API_KEYが設定されていません。"
                await msg.stream_token(answer_text)
                await msg.update()
                return
                
            stream = await anthropic_client.messages.create(
                model=model_info["value"],
                system=system_prompt,
                messages=[{"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content} for m in api_messages],
                max_tokens=4096,
                stream=True,
            )
            async for chunk in stream:
                if chunk.type == "content_block_delta":
                    token = chunk.delta.text or ""
                    answer_text += token
                    await msg.stream_token(token)

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        print(f"詳細エラー: {e}")
        
        # 修正点② content引数を使わずに更新
        msg.content = error_message
        await msg.update()
        
        # エラー時は最後のユーザーメッセージを履歴から削除
        if conversation_history and isinstance(conversation_history[-1], HumanMessage):
            cl.user_session.set("conversation_history", conversation_history[:-1])
        msg.content = error_message
        await msg.update()
