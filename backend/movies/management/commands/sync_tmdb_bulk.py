from django.core.management.base import BaseCommand
from movies.services.tmdb import fetch_and_sync_genre_master, sync_bulk_movies

class Command(BaseCommand):
    help = "TMDB discover/movie로 영화 다량(예: 500개) 동기화"

    def add_arguments(self, parser):
        parser.add_argument("--pages", type=int, default=25, help="페이지 수 (20*pages 만큼)")
        parser.add_argument("--sort", type=str, default="popularity.desc", help="TMDB sort_by")
        parser.add_argument("--with-credits", action="store_true", help="credits(감독/출연진)까지 동기화")
        parser.add_argument("--with-detail", action="store_true", help="detail(runtime/genres 보정)까지 동기화")
        parser.add_argument("--sleep", type=float, default=0.2, help="요청 간 sleep(초)")

    def handle(self, *args, **options):
        pages = options["pages"]
        sort_by = options["sort"]
        with_credits = options["with_credits"]
        with_detail = options["with_detail"]
        sleep_sec = options["sleep"]

        self.stdout.write(self.style.SUCCESS("1) Genre master 동기화..."))
        fetch_and_sync_genre_master()

        self.stdout.write(self.style.SUCCESS(f"2) Bulk movies 동기화... pages={pages} (≈{pages*20}개)"))
        total = sync_bulk_movies(
            pages=pages,
            sort_by=sort_by,
            with_credits=with_credits,
            with_detail=with_detail,
            sleep_sec=sleep_sec,
        )

        self.stdout.write(self.style.SUCCESS(f"✅ 완료: {total}개 upsert"))
