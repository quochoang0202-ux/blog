#!/usr/bin/env python3
"""Đồng bộ 05_Content (vault) → blog/content với tên file ASCII (không dấu).

Lý do: Quartz v5 lỗi emit trang có tên file chứa ký tự tiếng Việt có dấu
(chỉ tạo redirect, thiếu nội dung). Giải pháp: đổi tên file sang không dấu
khi copy, giữ nguyên title/aliases tiếng Việt trong frontmatter.

Cách dùng: python3 sync_blog_content.py
"""
import os
import re
import shutil
import unicodedata

VAULT_CONTENT = "/home/quochoang/Tài liệu/HoangOS/05_Content"
BLOG_CONTENT = "/home/quochoang/blog/content"


def to_ascii_slug(name: str) -> str:
    """Chuyển tên tiếng Việt có dấu → không dấu, thay space bằng -."""
    # Bỏ dấu tiếng Việt
    normalized = unicodedata.normalize("NFD", name)
    ascii_name = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
    # Giữ chữ Đ/đ
    ascii_name = ascii_name.replace("Đ", "D").replace("đ", "d")
    # Thay khoảng trắng và ký tự đặc biệt bằng -
    ascii_name = ascii_name.replace(" ", "-")
    ascii_name = re.sub(r"[^a-zA-Z0-9-]", "", ascii_name)
    ascii_name = re.sub(r"-+", "-", ascii_name)
    return ascii_name


def main():
    os.makedirs(BLOG_CONTENT, exist_ok=True)

    # Xóa content cũ trong blog
    for f in os.listdir(BLOG_CONTENT):
        os.remove(os.path.join(BLOG_CONTENT, f))

    copied = []
    for f in sorted(os.listdir(VAULT_CONTENT)):
        if not f.endswith(".md"):
            continue
        src = os.path.join(VAULT_CONTENT, f)
        # Tên mới: INDEX.md giữ nguyên, còn lại → không dấu
        if f == "INDEX.md":
            new_name = "INDEX.md"
        else:
            stem = f[:-3]
            new_name = to_ascii_slug(stem) + ".md"
        dst = os.path.join(BLOG_CONTENT, new_name)
        shutil.copy2(src, dst)
        copied.append((f, new_name))

    print(f"✅ Đã sync {len(copied)} files:")
    for old, new in copied:
        marker = " (giữ nguyên)" if old == new else ""
        print(f"  {old} → {new}{marker}")


if __name__ == "__main__":
    main()
