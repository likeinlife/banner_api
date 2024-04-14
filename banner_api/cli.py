import argparse as ap
import asyncio
import random
from dataclasses import dataclass

from container import Container
from dependency_injector.wiring import Provide, inject
from dto.banner import BannerContentDTO, PutBannerDTO
from uow import UnitOfWork


@dataclass
class Args:
    count: int


def parse_args() -> Args:
    parser = ap.ArgumentParser()

    parser.add_argument("count", type=int, default=10)

    args = parser.parse_args()
    return Args(count=args.count)


def setup_container() -> Container:
    container = Container()
    container.wire(modules=[__name__])
    container.init_resources()
    return container


def generate_content() -> BannerContentDTO:
    url = "http://" + "".join(random.choices("0123456789abcdefgigklmopqrstuvwxyz", k=8)) + ".com"
    title = "Title " + "".join(random.choices("0123456789abcdefgigklmopqrstuvwxyz", k=8))
    text = "Text " + "".join(random.choices("0123456789abcdefgigklmopqrstuvwxyz", k=8))
    return BannerContentDTO(title=title, text=text, url=url)


@inject
async def fill_database(count: int, uow: UnitOfWork = Provide[Container.uow]) -> None:
    async with uow:
        for _ in range(count):
            tag_ids = set(random.choices(range(1, 1000), k=100))
            feature_id = random.choice(range(1, 100000))
            is_active = bool(random.randint(0, 1))
            dto = PutBannerDTO(
                tag_ids=tag_ids,
                content=generate_content(),
                feature_id=feature_id,
                is_active=is_active,
            )
            await uow.banner.insert(dto)
        await uow.commit()


async def main():
    setup_container()
    args = parse_args()
    print("Start")  # noqa: T201
    await fill_database(args.count)
    print(f"Finish. Fill db with {args.count} banners")  # noqa: T201


if __name__ == "__main__":
    asyncio.run(main())
