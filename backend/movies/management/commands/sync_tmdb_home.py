# backend/movies/management/commands/sync_tmdb_home.py

from django.core.management.base import BaseCommand
from movies.services.tmdb import fetch_and_sync_genre_master, sync_home_section


class Command(BaseCommand):
    help = "TMDB 홈 섹션(POPULAR/NOW_PLAYING/TOP_RATED) 동기화"

    def add_arguments(self, parser):
        parser.add_argument("--pages", type=int, default=1, help="각 섹션당 가져올 페이지 수(기본 1)")
        parser.add_argument("--no-credits", action="store_true", help="credits(감독/출연진) 동기화 생략")

    def handle(self, *args, **options):
        pages = options["pages"]
        with_credits = not options["no_credits"]

        self.stdout.write(self.style.SUCCESS("1) Genre master 동기화..."))
        fetch_and_sync_genre_master()

        self.stdout.write(self.style.SUCCESS("2) POPULAR 동기화..."))
        sync_home_section("POPULAR", "/movie/popular", pages=pages, with_credits=with_credits)

        self.stdout.write(self.style.SUCCESS("3) NOW_PLAYING 동기화..."))
        sync_home_section("NOW_PLAYING", "/movie/now_playing", pages=pages, with_credits=with_credits)

        self.stdout.write(self.style.SUCCESS("4) TOP_RATED 동기화..."))
        sync_home_section("TOP_RATED", "/movie/top_rated", pages=pages, with_credits=with_credits)

        self.stdout.write(self.style.SUCCESS("✅ 완료"))
