import cream
import cream.ipc
import cream.extensions


class Mediaservice(cream.Module, cream.ipc.Object):
    def __init__(self):
        self.extension_api = {}

        cream.Module.__init__(self)
        cream.ipc.Object.__init__(self,
            'org.cream.mediaservice',
            '/org/cream/Mediaservice'
        )

        self.extension_manager.load_all()


if __name__ == '__main__':
    Mediaservice().main()
