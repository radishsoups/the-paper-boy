import json
import os
import re

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.news_agent import news_agent
from services.news_fetcher import fetch_news
from services.email_service import send_email

session_service = InMemorySessionService()


def extract_json(text: str):
    text = text.strip().replace("```json", "").replace("```", "")

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in output:\n{text}")

    return json.loads(match.group())


def format_email_html(date: str, summary_list: list) -> str:
    # Convert list to HTML bullet points
    bullet_html = ""
    if isinstance(summary_list, list):
        bullet_html = "<ul>" + "".join([
            f'<li style="margin:0 0 20px 0;color:rgb(54,55,55);line-height:26px;font-size:16px;margin-top:0">{item}</li>'
            for item in summary_list
        ]) + "</ul>"
    else:
        bullet_html = f'<p style="margin:0 0 20px 0;color:rgb(54,55,55);line-height:26px;font-size:16px;margin-top:0">{summary_list}</p>'

    return f"""
<html>
<body style="font-family: SF Pro Display, sans-serif; line-height: 1.6; color:#363737; background-color:#f5f5f5; margin:0; padding:0;">

    <!-- Outer wrapper -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center" style="padding: 20px 0;">

                <!-- Inner container -->
                <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff; padding: 32px;">
                    <tr>
                        <td>

                            <h2 style="font-size:32px; color:#363737; margin-top:0;">
                                good morning to you
                            </h2>

                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td valign="top">
                                        <p style="font-size:11px; color:#363737; line-height:1.6; margin:0;">THE PAPER BOY</p>
                                        <p style="font-size:11px; color:#767676; line-height:1.6; margin:0;">{date}</p>
                                    </td>
                                    <td width="40" valign="top" align="right">
                                        <img src="cid:icon.png" width="40" height="40" alt="icon" style="display:block; border-radius:50%;">
                                    </td>
                                </tr>
                            </table>

                            <hr style="height:1px; border-width:0; color:#e5e5e5; background-color:#e5e5e5; margin: 16px 0;">

                            <div>{bullet_html}</div>

                            <hr style="height:1px; border-width:0; color:#e5e5e5; background-color:#e5e5e5; margin: 16px 0;">

                            <p style="font-size:11px; color:#767676; line-height:1.6;">
                                brought to you by the paper boy. have a lovely day !
                            </p>

                        </td>
                    </tr>
                </table>

            </td>
        </tr>
    </table>

</body>
</html>
    """


async def run_daily_news(date: str):
    articles = fetch_news(date)

    print("ARTICLES COUNT:", len(articles))
    print("SAMPLE:", articles[:2])

    runner = Runner(
        app_name="news",
        agent=news_agent,
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="news",
        user_id="claire",
    )

    formatted_articles = "\n\n".join([
        f"""
Title: {a['title']}
Source: {a['source']}
Description: {a['description']}
URL: {a['url']}
""" for a in articles
    ])

    prompt = f"""
Summarize these tech news articles for {date}:

{formatted_articles}

Return ONLY valid JSON.
"""

    content = types.Content(
        role="user",
        parts=[types.Part(text=prompt)],
    )

    final_text = ""

    async for event in runner.run_async(
            user_id="claire",
            session_id=session.id,
            new_message=content,
    ):
        if event.is_final_response():
            final_text = event.content.parts[0].text

    if not final_text:
        raise ValueError("Agent returned empty response")

    result = extract_json(final_text)

    # Handle both list and string formats for summary
    summary = result["summary"]
    if isinstance(summary, str):
        # Parse string summary into bullet points
        summary = [s.strip() for s in summary.split("\n") if s.strip()]

    html_email = format_email_html(date, summary)
    image_path = os.path.join(os.path.dirname(__file__), "images", "icon.png")
    send_email(date, html_email, image_paths=[image_path])

    return result
