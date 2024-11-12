from django.core.management.base import BaseCommand
from articles.models import Article, Hashtag
from accounts.models import User
import random

class Command(BaseCommand):
    help = 'Generate diverse sample data for Article, Hashtag, and User models'

    def handle(self, *args, **kwargs):
        # 다채로운 해시태그 생성
        hashtag_names = [
            "맛집", "여행", "카페", "운동", "기술", "개발", "독서", "음악", "영화", "자연",
            "패션", "뷰티", "사진", "요리", "건강", "취미", "공부", "일상", "게임", "사진",
            "경제", "부동산", "자동차", "환경", "디자인", "예술", "문화", "과학", "역사", "철학"
        ]
        hashtag_objs = [Hashtag.objects.get_or_create(name=tag)[0] for tag in hashtag_names]
        
        # 샘플 유저 5명 생성
        usernames = ["user1", "user2", "user3", "user4", "user5"]
        users = []
        for username in usernames:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": f"{username}@example.com"}
            )
            if created:
                user.set_password("password")  # 비밀번호 설정
                user.save()
            users.append(user)

        # 다양한 제목과 내용 템플릿
        titles = [
            "오늘의 일상", "멋진 하루", "알아두면 좋은 팁", "나만의 비밀장소", "최고의 카페", "운동 루틴 공개",
            "기술 트렌드", "개발자의 삶", "주말 영화 추천", "자연의 아름다움", "여름 휴가 계획", "행복한 순간",
            "새로운 취미 찾기", "독서 리스트", "신나는 요리법", "친구와의 모임", "자전거 여행", "미래의 자동차",
            "환경 보호 실천", "디지털 시대의 공부법", "스마트한 경제생활", "인생 철학", "문화 탐방", "기분 좋은 노래",
            "영감을 주는 영화", "즐거운 하루를 위한 팁", "맛있는 집밥 요리", "쉽고 간편한 스트레칭", "자연과 함께하는 산책",
            "기술의 발전", "매일 성장하는 나"
        ]
        
        contents = [
            "이곳에서 커피를 마셨다.", "나만 알고 싶은 장소", "최신 기술은 언제나 놀랍다.", "개발이란 참 재미있다.",
            "여행은 언제나 즐거워.", "오늘 본 영화는 최고였다.", "자연 속에서 여유를 즐기다.", "독서는 마음을 풍요롭게 해준다.",
            "음악은 언제나 내 편이다.", "운동 후 상쾌한 기분!", "패션 트렌드를 따라가다.", "뷰티 팁 공유하기",
            "요즘 사진 찍기에 푹 빠졌다.", "오늘은 요리를 해볼까?", "건강을 지키기 위한 노력", "다양한 취미 즐기기",
            "공부가 가장 즐거운 시간", "게임의 세계로 빠져들다", "경제에 대한 이해를 넓히다", "자동차에 대해 알아보기",
            "환경 보호는 우리의 의무", "디자인에 대한 영감을 얻다", "역사적 사건을 되돌아보다", "과학에 대한 흥미를 높이다",
            "철학적인 대화를 나누다", "주변 사람들과의 소통 중요성", "창의력을 높이는 방법", "오늘도 한 걸음 성장",
            "유익한 정보를 공유하다.", "매일 작은 행복을 찾는다."
        ]

        # 50개의 샘플 Article 데이터 생성
        for i in range(30):
            title = random.choice(titles)
            content = f"{random.choice(contents)} 더 많은 이야기는 다음 기회에!"
            article = Article.objects.create(
                title=title,
                content=content,
                type=random.choice(["facebook", "twitter", "instagram", "threads"]),
                view_count=random.randint(0, 100),
                like_count=random.randint(0, 50),
                share_count=random.randint(0, 10)
            )
            # 해시태그 추가 (1~5개의 해시태그를 랜덤하게 선택)
            article.hashtags.set(random.sample(hashtag_objs, k=random.randint(1, 5)))
            article.save()

        self.stdout.write(self.style.SUCCESS("Successfully created 5 users, 30 diverse sample articles, and hashtags"))
