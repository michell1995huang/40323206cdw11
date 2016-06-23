from flask import Blueprint, request
 
bg5_40323206_1 = Blueprint('bg5_40323206_1', __name__, url_prefix='/bg5_40323206_1', template_folder='templates')

 
head_str = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 2D 鏈條繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/CangoAxes-1v33.js"></script>
 
</head>
<body>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id="plotarea" width="800" height="800"></canvas>
'''
 
tail_str = '''
</script>
</body>
</html>
'''
 
chain_str = '''
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window
import math
 
cango = JSConstructor(window.Cango)
cobj = JSConstructor(window.Cobj)
shapedefs = window.shapeDefs
obj2d = JSConstructor(window.Obj2D)
cgo = cango("plotarea")
 
cgo.setWorldCoords(-250, -250, 500, 500) 
 
# 畫軸線
cgo.drawAxes(0, 240, 0, 240, {
    "strokeColor":"#aaaaaa",
    "fillColor": "#aaaaaa",
    "xTickInterval": 20,
    "xLabelInterval": 20,
    "yTickInterval": 20,
    "yLabelInterval": 20})
 
deg = math.pi/180  
 
# 將繪製鏈條輪廓的內容寫成 class 物件
class chain():
    # 輪廓的外型設為 class variable
    chamber = "M -6.8397, -1.4894 \
            A 7, 7, 0, 1, 0, 6.8397, -1.4894 \
            A 40, 40, 0, 0, 1, 6.8397, -18.511 \
            A 7, 7, 0, 1, 0, -6.8397, -18.511 \
            A 40, 40, 0, 0, 1, -6.8397, -1.4894 z"
    cgoChamber = window.svgToCgoSVG(chamber)
 
    def __init__(self, fillcolor="green", border=True, strokecolor= "tan", linewidth=2, scale=1):
        self.fillcolor = fillcolor
        self.border = border
        self.strokecolor = strokecolor
        self.linewidth = linewidth
        self.scale = scale
 
    # 利用鏈條起點與終點定義繪圖
    def basic(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(math.atan2(y2-y1, x2-x1)/deg+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, self.scale, 0)
 
    # 利用鏈條起點與旋轉角度定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic_rot(self, x1, y1, rot, v=False):
        # 若 v 為 True 則為虛擬 chain, 不 render
        self.x1 = x1
        self.y1 = y1
        self.rot = rot
        self.v = v
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
        # 根據旋轉角度, 計算 x2 與 y2
        x2 = x1 + 20*math.cos(rot*deg)*self.scale
        y2 = y1 + 20*math.sin(rot*deg)*self.scale
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(rot+90)
 
        # 放大 scale 倍
        if v == False:
            cgo.render(basic1, x1, y1, self.scale, 0)
 
        return x2, y2
'''

# 傳繪 A 函式內容
def a(x, y, scale=1, color="green"):
    outstring = '''
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain(scale='''+str(scale)+''', fillcolor="'''+str(color)+'''")
 
# 畫 A
# 左邊兩個垂直單元
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+''', 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
# 左斜邊兩個單元
x3, y3 = mychain.basic_rot(x2, y2, 80)
x4, y4 = mychain.basic_rot(x3, y3, 71)
# 最上方水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜邊兩個單元
x6, y6 = mychain.basic_rot(x5, y5, -71)
x7, y7 = mychain.basic_rot(x6, y6, -80)
# 右邊兩個垂直單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
x9, y9 = mychain.basic_rot(x8, y8, -90)
# 中間兩個水平單元
x10, y10 = mychain.basic_rot(x8, y8, -180)
mychain.basic(x10, y10, x1, y1)
'''
 
    return outstring
    
@bg5_40323206_1.route('/a')
def draw_a():
    return head_str + chain_str + a(0, 0) + tail_str
def circle36(x, y, degree=10):
    # 20 為鏈條輪廓之圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    #degree = 10
    first_degree = 90 - degree
    repeat = 360 / degree
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
    return outstring
    
@bg5_40323206_1.route('/circle36/<degree>', defaults={'x': 0, 'y': 0})
@bg5_40323206_1.route('/circle36/<x>/<degree>', defaults={'y': 0})
@bg5_40323206_1.route('/circle36/<x>/<y>/<degree>')
#@ag100.route('/circle36/<int:x>/<int:y>/<int:degree>')
def drawcircle36(x,y,degree):
    return head_str + chain_str + circle36(int(x), int(y), int(degree)) + tail_str
@bg5_40323206_1.route('/hw_link')
def hw_link():
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 2D 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/CangoAxes-1v33.js"></script>
</head>
<body>
<script>
window.onload=function(){
brython(1);
}
</script>
<canvas id="plotarea" width="800" height="800"></canvas>
<script type="text/python">
from javascript import JSConstructor
from browser import window
import math
cango = JSConstructor(window.Cango)
cobj = JSConstructor(window.Cobj)
shapedefs = window.shapeDefs
obj2d = JSConstructor(window.Obj2D)
cgo = cango("plotarea")
cgo.setWorldCoords(-250, -250, 500, 500) 
        
#cgo.drawText("使用 Cango 繪圖程式庫!", 0, 0, {"fontSize":60, "fontWeight": 1200, "lorg":5 })
deg = math.pi/180  
def O(x, y, rx, ry, rot, color, border, linewidth):
    # 旋轉必須要針對相對中心 rot not working yet
    chamber = "M14.117 34.667 C16.826,36.432 20.949,37.194 24.186,37.329 C27.423,37.464 29.775,36.972 32.288,35.940 C34.801,34.908 37.477,33.336 38.814,26.290 A5.680,5.680 0 0,0 42.150,21.632 A5.680,5.680 0 0,0 39.731,16.437 A5.680,5.680 0 0,0 34.018,15.993 A5.680,5.680 0 0,0 34.345,10.240 A5.680,5.680 0 0,0 29.474,7.161 A5.680,5.680 0 0,0 24.417,9.925 A5.680,5.680 0 0,0 16.980,7.268 A5.680,5.680 0 0,0 14.076,14.613 A5.680,5.680 0 0,0 8.025,14.614 A5.680,5.680 0 0,0 5.408,20.070 A5.680,5.680 0 0,0 9.195,24.789 C10.112,30.136 11.407,32.903 14.117,34.667 M11.052 22.339 A2.918,2.918 0 0,1 8.133,19.421 A2.918,2.918 0 0,1 11.052,16.503 A2.918,2.918 0 0,1 13.970,19.421 A2.918,2.918 0 0,1 11.052,22.339 M19.325 15.360 A2.918,2.918 0 0,1 16.407,12.442 A2.918,2.918 0 0,1 19.325,9.524 A2.918,2.918 0 0,1 22.243,12.442 A2.918,2.918 0 0,1 19.325,15.360 M29.294 15.756 A2.918,2.918 0 0,1 26.376,12.838 A2.918,2.918 0 0,1 29.294,9.920 A2.918,2.918 0 0,1 32.212,12.838 A2.918,2.918 0 0,1 29.294,15.756 M36.494 24.023 A2.918,2.918 0 0,1 33.576,21.105 A2.918,2.918 0 0,1 36.494,18.187 A2.918,2.918 0 0,1 39.412,21.105 A2.918,2.918 0 0,1 36.494,24.023 M17.702 25.927 Q17.210,25.920 16.877,26.243 Q16.550,26.566 16.539,27.286 L16.498,30.006 L15.703,29.994 L15.749,26.952 Q15.757,26.422 15.565,26.160 Q15.373,25.892 14.938,25.886 Q14.603,25.881 14.310,26.053 Q14.024,26.219 13.893,26.558 Q13.761,26.897 13.752,27.534 L13.715,29.964 L12.920,29.952 L12.990,25.270 L13.703,25.280 L13.693,25.943 Q13.919,25.599 14.289,25.396 Q14.658,25.194 15.125,25.201 Q15.642,25.208 15.967,25.428 Q16.298,25.647 16.431,26.041 Q16.999,25.229 17.889,25.242 Q18.583,25.252 18.950,25.643 Q19.322,26.033 19.311,26.835 L19.263,30.047 L18.474,30.035 L18.518,27.088 Q18.525,26.608 18.452,26.399 Q18.380,26.190 18.173,26.060 Q17.973,25.931 17.702,25.927 M22.433 25.310 Q23.373,25.324 23.957,25.970 Q24.540,26.616 24.523,27.777 Q24.522,27.847 24.513,27.985 L21.024,27.933 Q21.056,28.710 21.441,29.126 Q21.833,29.536 22.420,29.545 Q22.855,29.551 23.162,29.329 Q23.474,29.106 23.665,28.604 L24.484,28.717 Q24.277,29.434 23.748,29.823 Q23.218,30.213 22.404,30.201 Q21.375,30.186 20.785,29.546 Q20.195,28.899 20.212,27.763 Q20.230,26.577 20.845,25.936 Q21.461,25.295 22.433,25.310 M29.585 27.796 Q29.571,28.698 29.292,29.212 Q29.013,29.725 28.491,30.008 Q27.970,30.284 27.358,30.275 Q26.373,30.260 25.777,29.620 Q25.180,28.980 25.198,27.794 Q25.217,26.494 25.946,25.880 Q26.560,25.371 27.431,25.384 Q28.396,25.399 28.999,26.039 Q29.602,26.679 29.585,27.796 M31.766 29.261 Q31.786,29.186 32.020,28.299 L32.806,25.565 L33.620,25.578 L34.280,28.308 L34.500,29.201 L34.785,28.303 L35.627,25.608 L36.397,25.619 L34.869,30.280 L34.042,30.267 L33.339,27.454 L33.168,26.657 L32.168,30.240 L31.341,30.227 L29.979,25.523 L30.799,25.535 L31.503,28.248 L31.766,29.261 z"
    cgoChamber = window.svgToCgoSVG(chamber)
    cmbr = cobj(cgoChamber, "SHAPE", {
            "fillColor": color,
            "border": border,
            "strokeColor": "tan",
            "lineWidth": linewidth })
            
            
            
    cmbr.translate(0, 20)    
            
 
   
    
    
    # hole 為原點位置
    #hole = cobj(shapedefs.circle(4), "PATH") 
    #cmbr.appendPath(hole) 
  
    # 放大 1 倍
    cgo.render(cmbr, x, y, 3, rot)
    
O(0, 0, 0, 0, 0, "green", False, 4)
</script>
'''
    return outstring
  
