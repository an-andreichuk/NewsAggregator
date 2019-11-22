namespace NewsAggregator.Utils
{
    public interface ITranslator
    {
        string TranslateText(string text, string language);
        string TranslateHtml(string text, string language);
    }
}
