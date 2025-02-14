import os
import json
import requests
import base64
import time

# تحميل التوكن واسم المستخدم من secrets
GITHUB_USERNAME = "GameGiftMaster"  # استبدل باسم المستخدم الخاص بك
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# قراءة جميع المقالات من مجلد "articles"
articles_dir = "articles"
if not os.path.exists(articles_dir):
    print(f"📁 المجلد '{articles_dir}' غير موجود!")
    exit(1)

# استرداد قائمة المقالات
articles = [f for f in os.listdir(articles_dir) if f.endswith(".md")]

def create_repo(repo_name):
    """إنشاء مستودع جديد لكل مقالة"""
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"name": repo_name, "private": False}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"✅ تم إنشاء المستودع: {repo_name}")
        return True
    elif response.status_code == 422:
        print(f"⚠️ المستودع '{repo_name}' موجود مسبقًا، سيتم تحديثه!")
        return True
    else:
        print(f"❌ فشل في إنشاء المستودع '{repo_name}': {response.text}")
        return False

def upload_article(repo_name, article_filename):
    """رفع المقالة إلى المستودع الخاص بها"""
    with open(f"{articles_dir}/{article_filename}", "r", encoding="utf-8") as file:
        content = file.read()

    encoded_content = base64.b64encode(content.encode()).decode()
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/{article_filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": f"إضافة المقالة: {article_filename}",
        "content": encoded_content
    }
    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        print(f"✅ تم رفع المقالة '{article_filename}' إلى المستودع '{repo_name}'")
    else:
        print(f"❌ فشل في رفع المقالة '{article_filename}': {response.text}")

# تنفيذ العملية لكل مقالة
for article in articles:
    repo_name = article.replace(".md", "").replace(" ", "-")  # اسم المستودع يكون اسم المقالة
    if create_repo(repo_name):
        time.sleep(2)  # انتظار قليل قبل رفع المقالة
        upload_article(repo_name, article)
