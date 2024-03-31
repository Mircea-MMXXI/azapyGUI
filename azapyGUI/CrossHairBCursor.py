class CrossHairBCursor:
    def __init__(self, ax, varx=None, vary=None,
                 transformx = lambda x: x, transformy = lambda y: y,
                 show_label=False):
        self._show_label = show_label
        self.varx = varx
        self.vary = vary
        self.transformx = transformx
        self.transformy = transformy
        self.set_ax(ax)
            

    def on_draw(self, event):
        self.create_new_background()
        
        
    def set_ax(self, ax):
        self.ax = ax
        x = ax.get_xlim()[1]
        y = ax.get_ylim()[1]
        if self.varx is not None: 
            self.varx.set(self.transformx(x))
        if self.vary is not None:   
            self.vary.set(self.transformy(y))
        
        self.background = None
        self.horizontal_line = ax.axhline(y, color='k', lw=0.8, ls='--')
        self.vertical_line = ax.axvline(x, color='k', lw=0.8, ls='--')
        if self._show_label: 
            self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)
        self._creating_background = False
        ax.figure.canvas.mpl_connect('draw_event', self.on_draw)


    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        if self._show_label:
            self.text.set_visible(visible)
        return need_redraw


    def create_new_background(self):
        if self._creating_background:
            return
        self._creating_background = True
        self.set_cross_hair_visible(False)
        self.ax.figure.canvas.draw()
        self.background = self.ax.figure.canvas.copy_from_bbox(self.ax.bbox)
        self.set_cross_hair_visible(True)
        self._creating_background = False


    def on_mouse_move(self, event):
        if self.background is None:
            self.create_new_background()
        if not event.inaxes:
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.restore_region(self.background)
                self.ax.figure.canvas.blit(self.ax.bbox)
        else:
            self.set_cross_hair_visible(True)
            x, y = event.xdata, event.ydata
            if self.varx is not None: 
                self.varx.set(self.transformx(x))
            if self.vary is not None:   
                self.vary.set(self.transformy(y)) 
            self.horizontal_line.set_ydata([y])
            self.vertical_line.set_xdata([x])
            if self._show_label:
                self.text.set_text(f'x={self._transformx(x)}, y={self._transformy(y)}')

            self.ax.figure.canvas.restore_region(self.background)
            self.ax.draw_artist(self.horizontal_line)
            self.ax.draw_artist(self.vertical_line)
            if self._show_label:
                self.ax.draw_artist(self.text)
            self.ax.figure.canvas.blit(self.ax.bbox)
