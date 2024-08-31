import random


def generate_html_content(reference, paired_lines):
    colors = [
        "red",
        "orange",
        "amber",
        "yellow",
        "lime",
        "green",
        "emerald",
        "teal",
        "cyan",
        "sky",
        "blue",
        "indigo",
        "violet",
        "purple",
        "fuchsia",
        "pink",
        "rose",
    ]
    color1, color2 = random.sample(colors, 2)

    content = "\n".join(
        f'<div class="mb-8">'
        f'<div class="text-right text-2xl sm:text-3xl md:text-4xl leading-relaxed text-gray-800 mb-2" dir="rtl">{h}</div>'
        f'<div class="text-left text-xl sm:text-2xl md:text-3xl leading-relaxed text-gray-700">{e}</div>'
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
        <style>
            body {{ font-family: 'Frank Ruhl Libre', serif; }}
        </style>
    </head>
    <body class="bg-gradient-to-br from-{color1}-100 to-{color2}-100 min-h-screen flex items-center justify-center p-4 sm:p-8 md:p-16">
        <div class="w-full max-w-4xl bg-white/80 backdrop-blur-sm rounded-xl shadow-2xl overflow-hidden">
            <div class="p-6 sm:p-10">
                <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold mb-6 text-center text-gray-800 border-b pb-4">{reference}</h1>
                <div class="space-y-8">
                    {content}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
