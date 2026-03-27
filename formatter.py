import os

def format_content():
    input_file = "kdp_draft_outline.md"
    output_dir = "dist"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(input_file, "r") as f:
        content = f.read()
    
    # --- A. Note / Web 用 HTML 変換 ---
    # 簡易的なタグ置換（prose-slate クラス対応）
    html_content = content.replace('### ', '<h3>').replace('## ', '<h2>').replace('# ', '<h1>')
    html_content = html_content.replace('\n', '<p>').replace('</p><p>', '</p>\n<p>')
    
    html_template = f"""
    <article class="prose prose-slate lg:prose-xl dark:prose-invert">
        {html_content}
    </article>
    """
    
    with open(f"{output_dir}/article.html", "w") as f:
        f.write(html_template)
        
    # --- B. Next.js / Content Factory 用 MDX 変換 ---
    with open(f"{output_dir}/article.mdx", "w") as f:
        f.write(content)

    print(f"Success: Formatted files saved in '{output_dir}/' directory.")

if __name__ == "__main__":
    format_content()
