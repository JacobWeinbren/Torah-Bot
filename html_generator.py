def generate_html_content(reference, paired_lines, color1, color2):
    content = "\n".join(
        f'<div class="mb-8">'
        f'<div class="text-right text-3xl leading-relaxed text-gray-800 mb-6" dir="rtl">{h}</div>'
        f'<div class="text-left text-2xl leading-relaxed text-gray-700">{e}</div>'
        f"</div>"
        for h, e in paired_lines
    )

    return f"""
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@400;700&display=swap" rel="stylesheet">
        <style>body {{ font-family: 'Frank Ruhl Libre', serif; }}</style>
    </head>
    <body class="bg-gradient-to-br from-[{color1}] to-[{color2}] min-h-screen flex items-center justify-center p-16">
        <div class="w-[800px] bg-white/90 backdrop-blur-sm rounded-2xl shadow-2xl overflow-hidden">
            <div class="px-12 py-8">
                <h1 class="text-4xl font-bold mb-12 text-center text-gray-800 border-b pb-8">{reference}</h1>
                <div class="space-y-16">{content}</div> 
            </div>
        </div>
    </body>
    </html>
    """
