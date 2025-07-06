from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai

# Google Generative AI API yapılandırması
genai.configure(api_key="GEMİNİ API KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        exam_choice = request.form.get("exam_choice")
        if exam_choice not in ["YKS", "LGS"]:
            return render_template("index.html", error="Geçersiz seçim. Lütfen YKS veya LGS seçin.")
        return redirect(url_for("menu", exam_choice=exam_choice))
    return render_template("index.html")

@app.route("/menu/<exam_choice>", methods=["GET", "POST"])
def menu(exam_choice):
    if request.method == "POST":
        option = request.form.get("option")
        if option == "1":
            return redirect(url_for("ask_question", exam_choice=exam_choice))
        elif option == "2":
            return redirect(url_for("analyze_test", exam_choice=exam_choice))
        elif option == "3":
            return redirect(url_for("create_schedule", exam_choice=exam_choice))
    return render_template("menu.html", exam_choice=exam_choice)

@app.route("/ask_question/<exam_choice>", methods=["GET", "POST"])
def ask_question(exam_choice):
    answer = None
    warning = None
    if request.method == "POST":
        question = request.form.get("question")
        goals = request.form.get("goals")

        if not question:
            warning = "Lütfen bir soru girin."
        else:
            # Hedeflerin kontrolü
            if goals:
                goals_list = [goal.strip() for goal in goals.split(",")]
                invalid_goals = [
                    goal for goal in goals_list
                    if (exam_choice == "YKS" and "LGS" in goal.upper()) or (exam_choice == "LGS" and "YKS" in goal.upper())
                ]

                if invalid_goals:
                    warning = f"Bu hedefler uygun değil: {', '.join(invalid_goals)}. Lütfen sadece {exam_choice} ile ilgili hedefler girin."
                else:
                    prompt = f"{exam_choice} için şu hedeflere yönelik bir soru: {goals_list}. Soru: {question}"
                    response = model.generate_content(prompt)
                    answer = response.text if response else "Yanıt alınamadı."
            else:
                prompt = f"{exam_choice} için: {question}"
                response = model.generate_content(prompt)
                answer = response.text if response else "Yanıt alınamadı."

    return render_template("ask_question.html", exam_choice=exam_choice, answer=answer, warning=warning)

@app.route("/analyze_test/<exam_choice>", methods=["GET", "POST"])
def analyze_test(exam_choice):
    if request.method == "POST":
        tyt_turkce = request.form.get("tyt_turkce")
        tyt_matematik = request.form.get("tyt_matematik")
        tyt_fen = request.form.get("tyt_fen")
        tyt_sosyal = request.form.get("tyt_sosyal")
        ayt_matematik = request.form.get("ayt_matematik")
        ayt_fizik = request.form.get("ayt_fizik")
        ayt_kimya = request.form.get("ayt_kimya")
        ayt_biyoloji = request.form.get("ayt_biyoloji")
        ayt_edebiyat = request.form.get("ayt_edebiyat")
        ayt_sosyal = request.form.get("ayt_sosyal")

        netler = {
            "TYT Türkçe": tyt_turkce,
            "TYT Matematik": tyt_matematik,
            "TYT Fen": tyt_fen,
            "TYT Sosyal": tyt_sosyal,
            "AYT Matematik": ayt_matematik,
            "AYT Fizik": ayt_fizik,
            "AYT Kimya": ayt_kimya,
            "AYT Biyoloji": ayt_biyoloji,
            "AYT Edebiyat": ayt_edebiyat,
            "AYT Sosyal": ayt_sosyal,
        }
        girilen_netler = {ders: net for ders, net in netler.items() if net}

        if not girilen_netler:
            return render_template("analyze_test.html", exam_choice=exam_choice, error="Lütfen en az bir net girin.")

        prompt = f"{exam_choice} için şu netleri analiz et: {girilen_netler}"
        response = model.generate_content(prompt)
        result = response.text if response else "Yanıt alınamadı."

        return render_template("result.html", exam_choice=exam_choice, result=result)

    return render_template("analyze_test.html", exam_choice=exam_choice)

@app.route("/create_schedule/<exam_choice>", methods=["GET", "POST"])
def create_schedule(exam_choice):
    if request.method == "POST":
        goals = request.form.get("goals")

        if not goals:
            return render_template("create_schedule.html", exam_choice=exam_choice, error="Lütfen hedeflerinizi girin.")

        goals_list = [goal.strip() for goal in goals.split(",")]
        invalid_goals = [
            goal for goal in goals_list
            if (exam_choice == "YKS" and "LGS" in goal.upper()) or (exam_choice == "LGS" and "YKS" in goal.upper())
        ]

        if invalid_goals:
            return render_template(
                "create_schedule.html",
                exam_choice=exam_choice,
                error=f"Bu hedefler uygun değil: {', '.join(invalid_goals)}. Lütfen sadece {exam_choice} ile ilgili hedefler girin."
            )

        prompt = f"{exam_choice} için şu hedeflere uygun bir çalışma programı oluştur: {goals_list}"
        response = model.generate_content(prompt)
        result = response.text if response else "Çalışma programı oluşturulamadı."

        return render_template("result.html", exam_choice=exam_choice, result=result)

    return render_template("create_schedule.html", exam_choice=exam_choice)

if __name__ == "__main__":
    app.run(debug=True)
