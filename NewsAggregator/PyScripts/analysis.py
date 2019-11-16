# -*- coding: utf8 -*-
import Algorithmia


class NewsAnalyser:
    def __init__(self):
        self.client = Algorithmia.client('simLnScRWPk7koh1Je5IZZP8Z7m1')

    def sentimentAnalysis(self, news):
        """
            Sentimental Analysis ( 'positive', 'neutral', 'negative')
        :param news: list of dictionaries
        :return: modified input list of dictionaries
        """
        if len(news) == 0:
            print("empty news")
            return []

        algo = self.client.algo('nlp/SentimentAnalysis/1.0.5')
        algo.set_options(timeout=100)

        for entry in news:
            input = {
                "document": entry['text'],
                "language": "uk"
            }

            sentiment = algo.pipe(input).result[0]['sentiment']

            if sentiment >= 0.4:
                sentiment = 'positive'
            elif sentiment >= -0.4:
                sentiment = 'neutral'
            else:
                sentiment = 'negative'

            entry['sentiment'] = sentiment

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
            input = entry['text']
            entry['keywords'] = algo.pipe(input).result

        return news


if __name__ == "__main__":
    test = NewsAnalyser()
    news = [{'text': "Олександр Гриценко був призначений на посаду голови правління 'Укрексімбанку' наглядовою радою фінустанови 1 серпня 2014 року. Колективу банку його представила особисто тодішня голова НБУ Валерія Гонтарева. Гриценко змінив на цій посаді Віталія Білоуса, який очолював 'Укрексімбанк' від початку 2013 року. Усі повноваження він отримав 15 серпня 2014 року – безстроково"}]
    test.sentimentAnalysis(news)
    test.autoTag(news)
    print(news[0]['keywords'])

    # client = Algorithmia.client('simLnScRWPk7koh1Je5IZZP8Z7m1')
    # input = "Нарцис вузьколистий росте в Україні лише на Закарпатті. Долина нарцисів – унікальна природна пам’ятка в урочищі Креші поблизу міста Хуст. Це єдине місце в Східній Європі, де існують природні зарості цієї білосніжної квітки. Схожі, але менші за площею популяції є ще в таких місцях: Альпах, Румунії, деяких країнах на Балканах. Науковці вважають, що багато тисячоліть тому, рятуючись від льодовика, квіти переселилися в хустську долину. Про це місце люди переповідають багато легенд. Одна з них є переспівом давньогрецького міфу про Нарциса. Друга легенда оповідає про татарське лихоліття. Коли ординці напали на Закарпаття та взяли приступом Хотинський замок, місцеві жителі припинили опір і піднесли в дарунок переможцям набиті нарцисовими квітами подушки як знак покори. Вороги зраділи, але вони, звісно, не знали, що нарцис – отруйна квітка, а той, хто засне на такій подушці, ніколи більше не прокинеться. Отже, уранці в ординському таборі мало хто побачив схід сонця. Нажахані подіями, татари втекли зі страшного краю. Долина в період цвітіння – незабутнє видовище. Цей феномен вартий того, аби хоч раз у житті його побачити."
    # input = "We live in the computer age, a world increasingly shaped by programmers. Who are they, what motivates them, and what impact will they have on the rest of us?\nThat impact is ever more visible. Everything around us is becoming computerized. Your typewriter is gone, replaced by a computer. Your phone has turned into a computer. So has your camera. Soon your TV and VCR will be components in a computer network. Your car has more processing power in it than a room-sized mainframe did in 1970. Letters, encyclopedias, newspapers, and even your local store are being replaced by the Internet. What's next?\nHackers & Painters examines the world of hackers and the motivations of the people who occupy it. In clear, thoughtful prose that draws on illuminating historical examples, Graham takes readers on a fast-moving tour of what he calls an intellectual Wild West.\nWhy do kids who can't master high school end up as some of the most powerful people in the world? What makes a startup succeed? Will technology create a gap between those who understand it and those who don't? Will Microsoft take over the Internet? What to do about spam?\nIf you want to understand what hackers are up to, this book will tell you. And if you are a hacker, you'll probably recognize in it a portrait of yourself."
    # algo = client.algo('SummarAI/Summarizer/0.1.3')
    # algo.set_options(timeout=300)  # optional
    # print(algo.pipe(input).result)
