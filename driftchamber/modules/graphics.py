from driftchamber.core.module import Module


class BasicDetectorView(Module):

    def event(self, datastore):
        detector = datastore.get('detector')

        for i, superlayer in enumerate(detector.superlayers):
            for layer in superlayer.layers:
                cells = [self._cell_view(cell, i) for cell in layer.cells]
                print(*cells, sep=' ')

    def _cell_view(self, cell, superlayer_index):
        symbols = ['o', 'x', 'O', 'X', ':', '.', 'I', '-', '#', '@']
        index = superlayer_index % len(symbols)

        return cell.width * symbols[index]
