# -*- coding: utf8 -*-
import Algorithmia
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class NewsAnalyser:
    def __init__(self):
        self.client = Algorithmia.client('simLnScRWPk7koh1Je5IZZP8Z7m1')
        self.sentimentAnalyser = SentimentIntensityAnalyzer()

    def sentimentAnalysis(self, news):
        """
            Sentimental Analysis ( 'positive', 'neutral', 'negative')
        :param news: list of dictionaries
        :return: modified input list of dictionaries
        """
        if len(news) == 0:
            print("empty news")
            return []

        # algo = self.client.algo('nlp/SentimentAnalysis/1.0.5')
        # algo.set_options(timeout=100)

        for entry in news:
            if "EnglishText" in entry and ("Sentiment" not in entry or entry["Sentiment"] is None):
                # input = {
                #     "document": entry['Text'],
                #     "language": "uk"
                # }
                #
                # sentiment = algo.pipe(input).result[0]['sentiment']
                sentiment = self.sentimentAnalyser.polarity_scores(entry["EnglishText"])["compound"]

                if sentiment >= 0.5:
                    sentiment = 'positive'
                elif sentiment >= 0:
                    sentiment = 'neutral'
                else:
                    sentiment = 'negative'

                entry['Sentiment'] = sentiment

        return news

    def autoTag(self, news):
        """
            Finding keywords of given list of news
        :param news: list of dictionaries
        :return: modified input list of dictionaries
        """

        if len(news) == 0:
            print("empty news")
            return []

        algo = self.client.algo('nlp/AutoTag/1.0.1')
        algo.set_options(timeout=100)

        for entry in news:
            if "EnglishText" in entry and ("KeyWords" not in entry or entry["KeyWords"] is None):
                input = entry['EnglishText']
                entry['KeyWords'] = algo.pipe(input).result

        return news

    def summary(self, news):
        """
        Get summary of EnglishText of every news
        :param news: list of dictionaries
        :return: modified input list of dictionaries
        """

        if len(news) == 0:
            print("empty news")
            return []

        algo = self.client.algo('nlp/Summarizer/0.1.8')
        algo.set_options(timeout=100)

        for entry in news:
            if "EnglishText" in entry and ("EnglishSummary" not in entry or entry["EnglishSummary"] is None):
                input = entry['EnglishText']
                entry['EnglishSummary'] = algo.pipe(input).result

        return news

    def lemmatizer(self, news):
        """
        Maps all words to their canonical forms for easier analysis
        :param news: list of dictionaries
        :return: modified input list of dictionaries
        """

        if len(news) == 0:
            print("empty news")
            return []

        algo = self.client.algo('StanfordNLP/Lemmatizer/0.1.0')
        algo.set_options(timeout=300)  # optional

        for entry in news:
            if "EnglishText" in entry and ("EnglishLemmas" not in entry or entry["EnglishLemmas"] is None):
                input = entry['EnglishText']
                entry['EnglishLemmas'] = algo.pipe(input).result

        return news

    def translateSummaryToUkr(self, news):
        """
        Translates EnglishSummary to Ukrainian
        :param news: list of dictionaries
        :return: modified input list of dictionaries
        """

        if len(news) == 0:
            print("empty news")
            return []

        algo = self.client.algo('translation/GoogleTranslate/0.1.1')
        algo.set_options(timeout=100)  # optional

        for entry in news:
            if "EnglishSummary" in entry and ("UkrSummary" not in entry or entry["UkrSummary"] is None):
                input = {
                    "action": "translate",
                    "text": entry['EnglishSummary'],
                    "target_language": "uk"
                }
                entry['UkrSummary'] = algo.pipe(input).result["translation"]

        return news


if __name__ == "__main__":
    # test = NewsAnalyser()
    # parser = argparse.ArgumentParser()
    # parser.add_argument("text", nargs='+')
    # news = [{'text': "Олександр Гриценко був призначений на посаду голови правління 'Укрексімбанку' наглядовою радою фінустанови 1 серпня 2014 року. Колективу банку його представила особисто тодішня голова НБУ Валерія Гонтарева. Гриценко змінив на цій посаді Віталія Білоуса, який очолював 'Укрексімбанк' від початку 2013 року. Усі повноваження він отримав 15 серпня 2014 року – безстроково"}]
    news = [{'text': "У вівторок зранку помер командир 128-ї гірсько-піхотної бригади Євген Коростельов, який був поранений на передовій кілька днів тому.\nЦю інформацію \"\nBBC News Україна\n\" підтвердили у штабі Об'єднаних сил.\nКомбриг помер близько 4-ї ранку 19 листопада.\nЄвген Коростельов був пораний 12 листопада біля Новотроїцького під час обходу передових позицій.\nВін разом із іншим офіцером \nпідірвався на міні.\n Повідомлялося про серйозні поранення ніг.\n13 листопада комбрига у важкому стані доправили до госпіталя у Харкові.\nВибухом Коростельову відірвало ліву стопу; права нога була повністю пошкоджена, але лікарі врятували її.\nПредставник Інформаційного агентства Міністерства оборони Дмитро Чалий підтвердив кореспонденту \nDepo.Харків\n: \"Сьогодні вночі помер. Стан його різко погіршився\".\nЧалий зазначив, що зараз встановлюється остаточна причина смерті.\nУ Мукачеві у зв’язку із загибеллю Коростельова 19 листопада оголошено Днем жалоби, розпорядився міський голова Андрій Балога.\nЄвген Коростельов став командиром 128-ї бригади лише у вересні цього року. До того він служив у 25-й десантній бригадій, де був начальником артилерії і заступником командира.\nМав звання полковника.\nУ Євгена Коростельова залишилася дружина, донька і син.\nЦе другий український комбриг, який загинув під час війни на Донбасі. Першим був командир 51-ї окремої механізованої бригади Павло Півоваренко, який загинув під час виходу з Іловайська"}]
    # test.sentimentAnalysis(news)
    # test.autoTag(news)
    # print(news[0]['keywords'])

    # client = Algorithmia.client('simLnScRWPk7koh1Je5IZZP8Z7m1')
    # input = "Нарцис вузьколистий росте в Україні лише на Закарпатті. Долина нарцисів – унікальна природна пам’ятка в урочищі Креші поблизу міста Хуст. Це єдине місце в Східній Європі, де існують природні зарості цієї білосніжної квітки. Схожі, але менші за площею популяції є ще в таких місцях: Альпах, Румунії, деяких країнах на Балканах. Науковці вважають, що багато тисячоліть тому, рятуючись від льодовика, квіти переселилися в хустську долину. Про це місце люди переповідають багато легенд. Одна з них є переспівом давньогрецького міфу про Нарциса. Друга легенда оповідає про татарське лихоліття. Коли ординці напали на Закарпаття та взяли приступом Хотинський замок, місцеві жителі припинили опір і піднесли в дарунок переможцям набиті нарцисовими квітами подушки як знак покори. Вороги зраділи, але вони, звісно, не знали, що нарцис – отруйна квітка, а той, хто засне на такій подушці, ніколи більше не прокинеться. Отже, уранці в ординському таборі мало хто побачив схід сонця. Нажахані подіями, татари втекли зі страшного краю. Долина в період цвітіння – незабутнє видовище. Цей феномен вартий того, аби хоч раз у житті його побачити."
    # input = "We live in the computer age, a world increasingly shaped by programmers. Who are they, what motivates them, and what impact will they have on the rest of us?\nThat impact is ever more visible. Everything around us is becoming computerized. Your typewriter is gone, replaced by a computer. Your phone has turned into a computer. So has your camera. Soon your TV and VCR will be components in a computer network. Your car has more processing power in it than a room-sized mainframe did in 1970. Letters, encyclopedias, newspapers, and even your local store are being replaced by the Internet. What's next?\nHackers & Painters examines the world of hackers and the motivations of the people who occupy it. In clear, thoughtful prose that draws on illuminating historical examples, Graham takes readers on a fast-moving tour of what he calls an intellectual Wild West.\nWhy do kids who can't master high school end up as some of the most powerful people in the world? What makes a startup succeed? Will technology create a gap between those who understand it and those who don't? Will Microsoft take over the Internet? What to do about spam?\nIf you want to understand what hackers are up to, this book will tell you. And if you are a hacker, you'll probably recognize in it a portrait of yourself."
    # algo = client.algo('SummarAI/Summarizer/0.1.3')
    # algo.set_options(timeout=300)  # optional
    # print(algo.pipe(input).result)
