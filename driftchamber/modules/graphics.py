from driftchamber.core.module import Module


class BasicDetectorView(Module):

    def event(self, datastore):
        detector = datastore.get('detector')

        for i, superlayer in enumerate(detector.superlayers):
            for layer in superlayer.layers:
                for cell in layer.cells:
                    print(self._show_cell_view(cell, i), end="")
                print('')

    def _show_cell_view(self, cell, cell_index):
        symbols = ['o', 'O', '0']
        index = cell_index % len(symbols)
        return cell.width * symbols[index]


class DetectorView(BasicDetectorView):

    def begin(self, datastore):
        self._datastore = datastore

    def _show_cell_view(self, cell, cell_index):
        if self._is_cell_hit(cell):
            symbols = ['x', 'X', 'X']
            index = cell_index * len(symbols)
            return cell.width * symbols[index]
        else:
            return super._show_cell_view(cell, cell_index)

    def _is_cell_hit(self, cell):
        hits = self._datastore.get('hits').filter(lambda hit: hit.cell == cell)
        return len(hits) > 0
