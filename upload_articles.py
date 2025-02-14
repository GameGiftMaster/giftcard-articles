import os
import json
import requests
import time

# تحميل Access Tokens من ملف JSON
with open("tokens.json") as f:
    tokens = json.load(f)

# إعدادات المستودعات
base_dir = "github_articles"
repo_name = "giftcard-articles"  # كل حساب لديه مستودع واحد بهذا الاسم

# رفع المقالات لكل حساب
for account_num, (account, token) in enumerate(tokens.items(), start=1):
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    # تحديد مجلد المقالات لهذا الحساب
    articles_folder = os.path.join(base_dir, f"account_{account_num}")

    if not os.path.exists(articles_folder):
        print(f"⚠️ المجلد {articles_folder} غير موجود، تخطي...")
        continue

    article_files = os.listdir(articles_folder)

    for article in article_files:
        file_path = os.path.join(articles_folder, article)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # رفع المقالة إلى المستودع
        github_url = f"https://api.github.com/repos/{account}/{repo_name}/contents/{article}"
        data = {
            "message": f"Added {article}",
            "content": content.encode("utf-8").hex(),
            "branch": "main"
        }
        response = requests.put(github_url, headers=headers, json=data)

        if response.status_code == 201:
            print(f"✅ {article} تم رفعه بنجاح إلى {repo_name} ({account})")
        elif response.status_code == 422:
            print(f"⚠️ {article} موجود بالفعل في {repo_name} ({account})")
        else:
            print(f"❌ فشل رفع {article} إلى {repo_name} ({account}): {response.json()}")

        # تأخير لمنع الحظر
        time.sleep(3600 / len(article_files))
