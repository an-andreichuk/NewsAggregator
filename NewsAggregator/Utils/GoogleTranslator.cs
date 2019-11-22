using Google.Cloud.Translation.V2;

namespace NewsAggregator.Utils
{
    public class GoogleTranslator : ITranslator
    {
        private readonly TranslationClient client;

        public GoogleTranslator()
        {
            client = TranslationClient.Create();
        }

        public string TranslateHtml(string text, string language)
        {
            var response = client.TranslateHtml(text, language);
            return response.TranslatedText;
        }

        public string TranslateText(string text, string language)
        {
            var response = client.TranslateText(text, language);
            return response.TranslatedText;
        }

    }
}
