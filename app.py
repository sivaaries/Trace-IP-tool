import wx
import wx.lib.platebtn as platebtn
import wx.grid as grd
import socket 
import threading 
from wx.adv import Animation, AnimationCtrl

class Tip(wx.Frame):  
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX| wx.TAB_TRAVERSAL))

############################################################################################### Read Console Display Size
        displaySize = wx.DisplaySize()
############################################################################################### Frame Properties        
        self.SetSize(wx.Size(displaySize[0]/5,displaySize[1]/1.1))
        self.SetTitle("Trace IP ")
        self.SetTransparent(200)
        self.Centre()
        self.SetBackgroundColour(wx.Colour('#ffffff'))
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("files\\tip.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)      
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_CLOSE, self._when_closed)
        self.main(displaySize)
############################################################################################### Using DC Paint Gradient filler for gradient effect for the panel
    def main(self,displaySize):
############################################################################################### Inititalizing Counter Variable for Gauge
        self.count = 0 
############################################################################################### Asigning Sizer
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
############################################################################################### Icon for the Application
        png = wx.Image('files\\Ico.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.pic = wx.StaticBitmap(self, -1, png, (5, 5), (png.GetWidth(), png.GetHeight()))
############################################################################################### Widgets
        self.conntd = Animation('files\\scan.gif')
        self.ctrl1 = AnimationCtrl(self, -1, self.conntd, pos=wx.Point(200,0))
        self.ctrl1.SetBackgroundColour(wx.Colour('#151f17'))        
        self.ctrl1.Stop()

        self.Status = wx.StaticText(self, size = (displaySize[0]/5, displaySize[1]/25),label="Waiting")
        self.Status.SetFont(wx.Font(10, wx.MODERN , wx.NORMAL, wx.BOLD))        
        self.Status.SetBackgroundColour(wx.Colour('#151f17'))
        self.Status.SetForegroundColour(wx.Colour('#ffffff'))

        self.Heading1 = wx.StaticText(self, size = (displaySize[0]/5, displaySize[1]/30),label='Trace IP')  
        self.Heading1.SetFont(wx.Font(12, wx.MODERN , wx.NORMAL, wx.BOLD))
        self.Heading1.SetBackgroundColour(wx.Colour('#151f17'))
        self.Heading1.SetForegroundColour(wx.Colour('#ffffff'))

        self.From_Adr = wx.StaticText(self,label='From')
        self.From_Adr.SetBackgroundColour(wx.Colour('#151f17'))
        self.From_Adr.SetForegroundColour(wx.Colour('#ffffff')) 
               
        self.To_Adr = wx.StaticText(self,label='To')
        self.To_Adr.SetBackgroundColour(wx.Colour('#151f17'))
        self.To_Adr.SetForegroundColour(wx.Colour('#ffffff')) 

        self.Start_Address = []
        for i in range(0,4):
            i = wx.TextCtrl(self,size=(25,20))

            self.Start_Address.append(i)
        
        self.End_Address = []
        for i in range(0,4):
            i = wx.TextCtrl(self,size=(25,20))
            self.End_Address.append(i)

############################################################################################### Button to iniate the scan
        self.Scan = platebtn.PlateButton(self,label='Scan', style=platebtn.PB_STYLE_GRADIENT|platebtn.PB_STYLE_NOBG)
        self.Scan.SetFont(wx.Font(12, wx.MODERN , wx.NORMAL, wx.BOLD))
        self.Scan.SetForegroundColour(wx.Colour('#ffffff'))        
        self.Scan.SetPressColor(wx.Colour('#19f205'))
        self.Scan.Bind(wx.EVT_BUTTON, self.scan)

############################################################################################### Grid for displaying the IP addresses

        self.IPs = grd.Grid(self,size=(displaySize[0]/5,displaySize[1]/1.5))
        self.IPs.EnableEditing( False )
        self.IPs.SetMargins( 0, 0 )
        self.IPs.EnableGridLines( True )
        self.IPs.EnableDragGridSize( False )
        self.IPs.EnableDragColMove( False )
        self.IPs.EnableDragColSize( True )
        self.IPs.SetColLabelSize( 30 )
        self.IPs.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        self.IPs.EnableDragRowSize( True )
        self.IPs.SetRowLabelSize( 25 )
        self.IPs.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )

        self.IPs.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP ) 
        self.IPs.CreateGrid(0,1)
        self.IPs.SetColLabelValue(0,"IP")      
        self.IPs.SetColSize(0,displaySize[0]/6.5)

        hbox1.Add(self.ctrl1,0,wx.ALIGN_CENTER)
        hbox1.Add(self.Status,0,wx.ALIGN_CENTER)
        hbox2.Add(self.pic, 0, wx.LEFT)
        hbox2.Add(self.Heading1, 0, wx.ALIGN_BOTTOM)
        hbox3.Add(self.From_Adr,0,wx.ALIGN_CENTER)
        hbox3.Add((displaySize[0]/10.5, displaySize[1]/30),1) 
        hbox3.Add(self.To_Adr,0,wx.ALIGN_CENTER)

        for i in range(0,4):
            hbox4.Add(self.Start_Address[i], 0, wx.ALIGN_CENTER) 

        hbox4.Add(self.Scan, 0, wx.ALIGN_CENTER)             
        hbox4.Add((displaySize[0]/50, displaySize[1]/30),1)  

        for i in range(0,4):
            hbox4.Add(self.End_Address[i], 0, wx.ALIGN_CENTER)   

############################################################################################### Sizer
        vbox.Add(hbox1)
        vbox.Add(hbox2)
        vbox.Add(hbox3)        
        vbox.Add(hbox4) 

        vbox.Add(((displaySize[0]/30, displaySize[1]/30)),1)
        vbox.Add(self.IPs, 0, wx.ALIGN_CENTER)
        
        self.SetSizer(vbox)

############################################################################################### Threading
    def scan(self,event):
        t1 = threading.Thread(target=self.start)
        self.ctrl1.Play()
        self.Status.SetLabel("Scanning")
        t1.start() 
############################################################################################### Socket function 
    def start(self):
############################################################################################### Socket initiation        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        i = 0
############################################################################################### Incrementing IP number from the user defined range
        try:
            ping0 = self.Start_Address[2].GetValue()
            for ping in range(int(self.Start_Address[3].GetValue()),int(self.End_Address[3].GetValue())):
                address = '192.168.' + str(ping0) + "." + str(ping)
                result = sock.connect_ex((address,8080))

                if result == 10061:
                    self.IPs.AppendRows(1,updateLabels=True)
                    self.IPs.SetCellValue(i,0,address)

                    i+=1
                    self.ctrl1.Stop()
                    self.Status.SetLabel("Finished")
                else:

                    self.ctrl1.Stop()
        except:
            sock.close()
############################################################################################### Close Event to Destroy App when closed            
    def _when_closed(self,event):
        self.Destroy()


    def on_paint(self, event):
############################################################################################### establish the painting canvas
        dc = wx.PaintDC(self)
        x = 0
        y = 0
        w, h = self.GetSize()
        dc.GradientFillLinear((x, y, w, h), '#000000', '#A9A9A9')

def main():
    app = wx.App()
    ex = Tip(None)
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
