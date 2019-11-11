import wx
import rasterio
from rasterio.merge import merge
import glob
import os

class myFrame(wx.Frame):

    # 结构函数，这样就没必要每次都要单独执行一下
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, '图像拼接', size=(700, 300))
        # 上面这个就是直接弹出这个框的用的 初始化用的，  这样就是不用 用命令的

        # making a  panel
        panel = wx.Panel(self)  # self
        button = wx.Button(panel, label='运行', pos=(250, 200), size=(180, 35))

        wx.StaticText(panel, -1, "请输入文件路径:", pos=(25, 45))
        wx.StaticText(panel, -1, "请输入EPSG Code:", pos=(25, 113))
        wx.StaticText(panel, -1, "EPSG Code 请访问网址 epsg.io 进行查询\n例如:WGS84 UTM 50N的EPSG Code为 EPSG:32650", pos=(135, 150))
        wx.StaticText(panel, -1, "Author：CAF_IFRIF_Mr.mu\n\n                              V:1.0", pos=(500, 190))

        self.Bind(wx.EVT_BUTTON, self.closebutton, button)
        self.path = wx.TextCtrl(panel, -1, "", pos=(135, 40), size=(500, 25))
        self.epsg = wx.TextCtrl(panel, 1, "", pos=(135, 110), size=(250, 25))
        self.Bind(wx.EVT_CLOSE, self.closewindow)
        # 三个参数分别是干嘛的 ：
        # 第一个 表示类型是 按键按一下
        # 第二个 表示的是 做什么事情，这是函数需要自己去写
        # 第三个参数表示的应用在哪个东西上 这里是应用在button上这个按键

    def closebutton(self, event):
        dirpath = self.path.GetValue()
        out_fp = os.path.join(self.path.GetValue(),'mosaic.tif')

        search_criteria = "*.tif"
        q = os.path.join(dirpath, search_criteria)
        tif_fps = glob.glob(q)

        # define projection
        dst_crs = self.epsg.GetValue()  # CRS for web meractor

        src_files_to_mosaic = []

        for fp in tif_fps:
            src = rasterio.open(fp)
            src_files_to_mosaic.append(src)

        src_files_to_mosaic
        mosaic, out_trans = merge(src_files_to_mosaic)
        out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                         "height": mosaic.shape[1],
                         "width": mosaic.shape[2],
                         "transform": out_trans,
                         "crs": dst_crs
                         }
                        )
        with rasterio.open(out_fp, "w", **out_meta) as dest:
          dest.write(mosaic)


        self.Close(True)

    def closewindow(self, event):
         self.Destroy()  # Detroy  class




if __name__ == '__main__':
    app = wx.App()
    frame = myFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()


