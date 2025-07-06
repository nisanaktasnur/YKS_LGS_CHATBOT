# YKS_LGS_CHATBOT – Gemini API Destekli Eğitim Asistanı

Bu proje, YKS ve LGS sınavlarına hazırlanan öğrenciler için kişiselleştirilmiş konu önerileri, net analizi ve çalışma programı sunan bir yapay zekâ destekli web uygulamasıdır.  
Uygulama, **Google Gemini API** kullanılarak geliştirilen Python tabanlı bir **Flask uygulamasıdır**.

---

## Özellikler

- **Gemini API entegrasyonu**: Doğal dil işleme ile konu ve hedef analizleri
- **Sınav seçimi (YKS/LGS)**: Kullanıcıya özel içerik üretimi
- **Soru yanıtlama**: Öğrencinin hedeflerine uygun örnek soru üretimi
- **Test net analizi**: TYT / AYT netlerine göre konuya özel geribildirim
- **Çalışma programı oluşturma**: Öğrencinin hedeflerine göre haftalık plan

---

## API Anahtarı Kullanımı (Gemini API Key)

Uygulama, Gemini API ile etkileşim kurmak için bir API anahtarı kullanır.  
API anahtarı güvenlik amacıyla doğrudan koda yazılmak yerine **bir `.env` dosyasında** saklanmalıdır.

### Örnek:
```python
import google.generativeai as genai
genai.configure(api_key="GEMINI API KEY")  # senin özel anahtarın burada tanımlanır
