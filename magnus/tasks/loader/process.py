from tasks.core.sources import OneDriveDS


class LoaderProcess:
    def __init__(self) -> None:
        self.__sources = [OneDriveDS()]

    def run(self):
        for source in self.__sources:
            source.run()
