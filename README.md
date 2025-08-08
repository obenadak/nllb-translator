# TR-ENG-ES Çeviri Asistanı

Bu proje, Meta AI tarafından geliştirilen `facebook/nllb-200-distilled-600M` modelini kullanarak Türkçe, İngilizce ve İspanyolca metinleri bu dilelr arasında çeviren bir web uygulamasıdır. Arayüz, Gradio kütüphanesi ile oluşturulmuştur.

## Özellikler

- **Yüksek Kaliteli Çeviri:** Facebook'un NLLB (No Language Left Behind) modelini kullanır.
- **Etkileşimli Arayüz:** Temiz ve kullanımı kolay bir arayüz.
- **Dil Değiştirme:** Tek tıkla kaynak ve hedef dilleri ve metinleri takas etme.
- **Dinamik Yükleme:** Uygulama açılırken modelin yüklenme durumunu gösterir.
- **Özel Tema:** Modern ve karanlık bir tema ile şık bir görünüm.

## Yerel Makinede Çalıştırma

1.  Projeyi klonlayın:
    ```bash
    git clone https://github.com/obenadak/nllb-translator.git
    cd nllb-translator
    ```

2.  Gerekli kütüphaneleri kurun:
    ```bash
    pip install -r requirements.txt
    ```

3.  Uygulamayı çalıştırın:
    ```bash
    python app.py
    ```

## 🔗 Hugging Face Demo

Uygulamayı canlı olarak denemek için aşağıdaki Hugging Face Space'i ziyaret edebilirsiniz:

**https://huggingface.co/spaces/obenadak/nllb-translator**