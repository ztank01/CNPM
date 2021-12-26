import math
from typing import Union

from flask import render_template, request, jsonify
from flask_login import login_user

from admin import *
from my_app import my_login, utils
from my_app.models import TaiKhoanNhanVien, DanhGiaCuaKhach
from my_app.momo import momoRequestJSON
from my_app.utils import *

msg = ""
err_msg = ""
heso = ThongSoQuyDinh.query.all()[0].GiaTri
tylephuthu = ThongSoQuyDinh.query.all()[1].GiaTri


@app.route("/")
def home():
    MaLoaiPhong = request.args.get("MaLoaiPhong")
    if session.get('khach'):
        Phong = utils.get_Phong(kw=request.args.get("kw"),
                                MaLoaiPhong=MaLoaiPhong,
                                page=int(request.args.get("page", 1)))

        count = utils.count_Phong(MaLoaiPhong=request.args.get("MaLoaiPhong"), kw=request.args.get("kw"))
        size = app.config["PAGE_SIZE"]
    else:
        Phong = utils.get_PhongTrong(kw=request.args.get("kw"),
                                     MaLoaiPhong=MaLoaiPhong,
                                     page=int(request.args.get("page", 1)))
        TinhTrang = 'FR'

        count = utils.count_Phong(MaLoaiPhong=request.args.get("MaLoaiPhong"), TinhTrang=TinhTrang,
                                  kw=request.args.get("kw"))
        size = app.config["PAGE_SIZE"]

    return render_template("home.html", Phong=Phong, MaLoaiPhong=MaLoaiPhong,
                           page_num=math.ceil(count / size), kw=request.args.get("kw"))


@app.route("/dangnhap")
def dangnhap():
    return render_template("layout/login.html", err_msg=err_msg)


@app.route("/dangxuat")
def dangxuat():
    logout_user()
    del session['khach']
    return redirect("/")


@app.route("/tra_phong_truc_tuyen")
def traPhongTrucTuyen():
    if current_user.is_authenticated:
        rooms = getAllRoomByUserID()
        new_list = []
        for row in rooms:
            new_row = list(row)
            new_row.append(soNgayO(row[0].NgayBatDau))
            new_row.append(price(row[0].NgayBatDau, row[2].DonGia))
            new_list.append(tuple(new_row))
        priceAllRooms = totalPrice(new_list)
        return render_template("layout/traphong.html", rooms=new_list, priceAllRooms=priceAllRooms)
    else:
        global msg
        msg = "Bạn phải đăng nhập để trả phòng"
        return redirect("/")


@app.route("/api/thanhtoan_online", methods=["post"])
def getLink():
    rooms = getAllRoomByUserID()
    new_list = []
    for row in rooms:
        new_row = list(row)
        new_row.append(soNgayO(row[0].NgayBatDau))
        new_row.append(price(row[0].NgayBatDau, row[2].DonGia))
        new_list.append(tuple(new_row))
    priceAllRooms = totalPrice(new_list)
    amount = str(priceAllRooms)
    info = ''
    phong = ''
    for row in new_list:
        info = info + str(row[0].MaHopDong) + ","
        phong = phong + str(row[0].MaPhong) + ","
    info = info[:-1]
    phong = phong[:-1]
    orderInfo = "Thanh toán phòng " + phong
    print(amount, orderInfo, info)
    payLink = momoRequestJSON(amount=amount, orderInfo=orderInfo, hopdong=info)

    return redirect(payLink)


@app.route("/thanh_toan_thanh_cong")
def thanhToanThanhCong():
    data = request.json
    resultCode = data['resultCode']
    msg = "false"
    # Kiểm tra resultCode
    if resultCode == 0:
        rooms = getAllRoomByUserID()
        new_list = []
        for row in rooms:
            new_row = list(row)
            new_row.append(soNgayO(row[0].NgayBatDau))
            new_row.append(price(row[0].NgayBatDau, row[2].DonGia))
            new_list.append(tuple(new_row))
            print(row[0].MaHopDong)
        for i in range(new_list):
            hoadon = HoaDon(MaHopDong=new_list[i], ThanhTien=new_list[i][4])
            db.session.add(hoadon)
            db.session.commit()
            db.session.query(Phong).filter(Phong.MaPhong == new_list[i].MaPhong).update({Phong.TinhTrang: "FR"})
            db.session.commit()
        msg = 'true'
    return render_template("layout/PaymentSuccess.html", msg=msg)


@my_login.user_loader
def user_load(user_id):
    return TaiKhoanNhanVien.query.get(user_id)


@app.route("/login", methods=['get', 'post'])
def login_exe():
    redirectString = '/dangnhap'  # Để link của trang login
    username = request.form.get("username")
    password = request.form.get("password")
    password = str(hashlib.md5(password.encode("utf-8")).digest())

    user = TaiKhoanKhach.query.filter(TaiKhoanKhach.username == username,
                                      TaiKhoanKhach.password == password).first()
    if user:  # dang nhap thanh cong
        login_user(user=user)
        sessionKhach = {'khach': {
            "username": username,
            "password": password,
            'id': user.get_id()
        }
        }
        session['khach'] = sessionKhach
        redirectString = '/'
    else:
        user = TaiKhoanNhanVien.query.filter(TaiKhoanNhanVien.username == username,
                                             TaiKhoanNhanVien.password == password,
                                             TaiKhoanNhanVien.active == 1).first()
        if user:
            login_user(user=user)
            sessionKhach = {'khach': {
                "username": username,
                "password": password,
                'id': user.get_id()
            }
            }
            session['khach'] = sessionKhach
            redirectString = '/nhanvien'
            user = TaiKhoanNhanVien.query.filter(TaiKhoanNhanVien.username == username,
                                                 TaiKhoanNhanVien.password == password,
                                                 TaiKhoanNhanVien.emp_id == TaiKhoanAdmin.emp_id,
                                                 TaiKhoanNhanVien.active == 1).first()
            if user:  # dang nhap thanh cong
                login_user(user=user)
                redirectString = '/admin'
        else:
            global err_msg
            err_msg = "Username hoặc Password không chính xác!!!"

    return redirect(redirectString)


@app.route("/nhanvien")
def NhanVien():
    return render_template("layout/NhanVien.html")


# dùng để load trang lập phiếu thêu phòng
@app.route("/thuephong")
def thue():
    phong = Phong.query.all()
    return render_template("layout/LapPhieuThuePhong.html", phong=phong)


# dùng để update lên database chi tiết thuê
@app.route("/xacnhan", methods=['post'])
def hopdong():
    phong = request.form.get("phong")
    khachhang = request.form.get("khachhang")
    ngaydukien = request.form.get("songay")
    cmnd = request.form.get("cmnd")
    diachi = request.form.get("diachi")
    SoLuongKhach = db.session.query(ChiTietThue.MaPhong).filter(
        ~exists().where(ChiTietThue.MaHopDong == HoaDon.MaHopDong)).all()
    dem = 0
    for x in SoLuongKhach:
        if x[0] == int(phong):
            dem = dem + 1
    if dem < 3:
        # nếu chưa có trong danh sách khách thì lệnh này insert vào bảng khách
        ktr = Khach.query.filter(Khach.MaKhach == khachhang).all()
        if not ktr:
            khach = Khach(MaKhach=khachhang, MaLoaiKhach=request.form.get("loaikhach"), CMND=cmnd, DiaChi=diachi)
            db.session.add(khach)
            db.session.commit()
        db.session.query(Phong).filter(Phong.MaPhong == phong).update({Phong.TinhTrang: "IU"})
        db.session.commit()
        chitietthue = ChiTietThue(MaPhong=phong, MaKhach=khachhang, SoNgayODuKien=ngaydukien)
        db.session.add(chitietthue)
        db.session.commit()
        return render_template("layout/NhanVien.html")
    else:
        return render_template("layout/thongbaothuephong.html")


# load trang lập hóa đơn
@app.route("/hoadon")
def laphoadon():
    global tylephuthu
    mahopdong = db.session.query(ChiTietThue.MaHopDong).filter(
        ~exists().where(ChiTietThue.MaHopDong == HoaDon.MaHopDong)).all()
    phong = Phong.query.all()
    mahoadon = request.args.get("mahopdong")
    hopdong = utils.get_laphoadon(mahopdong=mahoadon)
    TimKhachThu3 = db.session.query(ChiTietThue.MaPhong, ChiTietThue.MaHopDong).filter(
        ~exists().where(ChiTietThue.MaHopDong == HoaDon.MaHopDong)).all()
    khach3 = db.session.query(ChiTietThue.MaPhong, ChiTietThue.MaHopDong).filter(
        ChiTietThue.MaHopDong == mahoadon).all()
    thongbao = []
    if khach3:
        dem = 0
        for x in TimKhachThu3:
            if x[0] == khach3[-1][0]:
                dem = dem + 1
            if x[0] == khach3[-1][0] and x[1] == khach3[-1][1] and dem == 3:
                for a in range(0, len(hopdong)):
                    if hopdong[a][2] == x[1]:
                        new_row = list()
                        new_row.append(hopdong[a][0])
                        new_row.append(hopdong[a][1])
                        new_row.append(hopdong[a][2])
                        new_row.append(hopdong[a][3])
                        new_row.append(hopdong[a][4])
                        new_row.append(hopdong[a][5] * (tylephuthu + 1))
                        hopdong[a] = new_row
                        btbao = list()
                        btbao.append(x[1])
                        btbao.append("Khách thứ 3 nên phụ thu thêm " + str(tylephuthu * 100) + "%")
                        thongbao.append(btbao)
                        dem = 0
                        break

    if not hopdong:
        return render_template("layout/thongbaohoadon.html")
    else:
        return render_template("layout/LapHoaDon.html", phong=phong, mahopdong=mahopdong, hopdong=hopdong, heso=heso,
                               thongbao=thongbao)


# dùng để lấy giá trị tổng tiền và upload database hóa đơn
@app.route("/laphoadon")
def hoadon():
    thanhtien = request.args.get("thanhtien")
    mahopdong = request.args.get("mahopdong")
    hoadon = HoaDon(MaHopDong=mahopdong, ThanhTien=thanhtien)
    db.session.add(hoadon)
    db.session.commit()
    phong = db.session.query(ChiTietThue.MaPhong).filter(
        ~exists().where(ChiTietThue.MaHopDong == HoaDon.MaHopDong)).all()
    phongtt = db.session.query(ChiTietThue.MaPhong).filter(ChiTietThue.MaHopDong == mahopdong).all()
    dem = 0
    for i in phong:
        if i[0] == phong[-1][0]:
            dem = dem + 1
    if dem == 0:
        db.session.query(Phong).filter(Phong.MaPhong == phongtt[-1][0]).update({Phong.TinhTrang: "FR"})
        db.session.commit()
    return render_template("layout/NhanVien.html")


@app.route("/baocao")
def baocao():
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    bcao = utils.get_tongtien(from_date=from_date, to_date=to_date)
    tongdoanhthu = utils.get_tongtile(from_date=from_date, to_date=to_date)
    return render_template("layout/LapBaoCaoThang.html", bcao=bcao, tongdoanhthu=tongdoanhthu)


@app.route("/matdo")
def baocaomatdo():
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    phongdatt = utils.get_phongdatt(from_date=from_date, to_date=to_date)
    phongchuatt = utils.get_phongchuatt(from_date=from_date, to_date=to_date)
    new_list = []
    tongngay = 0
    for i in phongdatt:
        new_row = list()
        new_row.append(i[0])
        new_row.append(i[1])
        tongngay = tongngay + i[1]
        new_list.append((new_row))
    for j in phongchuatt:
        new_row = list()
        new_row.append(j[0].MaPhong)
        new_row.append(utils.get_songaychuatt(j[0].NgayBatDau, j[1].NgayTraPhong))
        tongngay = tongngay + utils.get_songaychuatt(j[0].NgayBatDau, j[1].NgayTraPhong)
        new_list.append((new_row))
    finallist = []
    for x in range(0, len(new_list)):
        new_row = list()
        a = 0
        for y in range(x, len(new_list)):
            if new_list[x][0] == new_list[y][0]:
                a = a + new_list[y][1]
        dem = 0
        for b in range(0, len(finallist)):
            if new_list[x][0] == finallist[b][0]:
                dem = dem + 1
        if dem == 0:
            new_row.append(new_list[x][0])
            new_row.append(a)
            finallist.append(new_row)
    return render_template("layout/BaoCaoMatDo.html", matdo=finallist, tile=tongngay)


# load trang đánh giá
@app.route("/danhgia")
def danhgiasao():
    khach = Khach.query.all()
    phong = Phong.query.all()
    return render_template("layout/DanhGiaChatLuong.html", phong=phong, khach=khach)


# lưu đánh giá về database
@app.route("/updateDG", methods=['post'])
def updateDanhGia():
    khach = request.form.get("khach")
    phong = request.form.get("phong")
    nhanxet = request.form.get("nhanxet")
    ngaydg = request.form.get("ngaydg")
    sosao = request.form.get("SoSao")
    DanhGia = DanhGiaCuaKhach(MaPhong=phong, MaKhach=khach, NgayBatDau=ngaydg, NoiDung=nhanxet, SoSao=sosao)
    db.session.add(DanhGia)
    db.session.commit()
    return render_template("layout/DanhGiaChatLuong.html")


@app.route("/api/pay", methods=['post'])
def pay():
    cart = session.get('cart')
    print(cart)
    if cart:
        for p in cart:
            print(p)
            if not kiemTraPhongTrong(p):
                return jsonify({
                    "msg": p,
                    "error_code": 400
                })
        if add_HoaDon_ChiTietThue(cart):
            del session['cart']

            return jsonify({
                "error_code": 200
            })

    return jsonify({
        "error_code": 404
    })


@app.route("/api/update-cart-item", methods=['put'])
def update_cart_item():
    cart = session.get("cart")
    print(cart)

    if cart:
        data = request.json
        print(data)
        try:
            maPhong = str(data['MaPhong'])
            ngayBatDau = data['NgayBatDau']
            print(ngayBatDau)
            quantity = data['quantity']
        except Union[IndexError, KeyError] as ex:
            print(ex)
        else:
            if quantity > 0:
                if maPhong in cart:
                    p = cart[maPhong]
                    p['quantity'] = quantity
                    p['NgayBatDau'] = ngayBatDau

                    session["cart"] = cart

                    return jsonify({
                        "error_code": 200,
                        "cart_stats": utils.cart_stats(cart)
                    })

    return jsonify({
        "error_code": 404
    })


@app.context_processor
def common_context():
    LoaiPhong = utils.get_LoaiPhong()
    cart_stats = utils.cart_stats(session.get('cart'))

    return {
        "LoaiPhong": LoaiPhong,
        "cart_stats": cart_stats
    }


@app.route("/cart")
def cart():
    cart_stats = utils.cart_stats(session.get('cart'))

    return render_template("layout/cart.html",
                           cart_stats=cart_stats)


@app.route("/api/delete-cart-item/<MaPhong>", methods=['delete'])
def delete_cart_item(MaPhong):
    cart = session.get('cart')
    if cart:
        if MaPhong in cart:
            del cart[MaPhong]
            session["cart"] = cart

            return jsonify({
                "error_code": 200,
                "cart_stats": utils.cart_stats(cart)
            })

    return jsonify({
        "error_code": 404
    })


@app.route("/api/add-item-cart", methods=['post'])
def add_to_cart():
    cart = session.get("cart")
    if not cart:
        cart = {}

    data = request.json
    maPhong = str(data["MaPhong"])
    maLoaiPhong = data["MaLoaiPhong"]
    loaiPhong = utils.get_LoaiPhong(maLoaiPhong)[0]

    if maPhong in cart:
        p = cart[maPhong]
        p['quantity'] += 1
    else:
        cart[maPhong] = {
            "MaPhong": data["MaPhong"],
            "LoaiPhong": loaiPhong.LoaiPhong,
            "DonGia": loaiPhong.DonGia,
            "NgayBatDau": str(datetime.date.today()),
            "quantity": 1
        }

    session["cart"] = cart

    return jsonify(utils.cart_stats(cart))


@app.route("/register", methods=['get', 'post'])
def register():
    loaiKhach = utils.get_LoaiKhach()
    err_msg = ""
    if request.method == 'POST':
        try:
            username = request.form["username"]
            password = request.form["password"]
            confirm_password = request.form["confirm-password"]
            if password.strip() == confirm_password.strip():

                maLoaiKhach = request.form["LoaiKhach"]
                CMND = request.form["CMND"]
                diaChi = request.form["DiaChi"]
                ngaySinh = request.form["NgaySinh"]
                SDT = request.form["SDT"]
                loaiSDT = request.form["LoaiSDT"]

                if utils.exist_taiKhoan(username):
                    err_msg = "username và password đã tồn tại!! Vui lòng đổi username và password khác"
                else:
                    if utils.add_Khach(username, password, maLoaiKhach, CMND, diaChi, ngaySinh, SDT, loaiSDT):
                        return redirect("/dangnhap")
                    else:
                        err_msg = "Dữ liệu đầu vào không hợp lệ!"
            else:
                err_msg = "Mật khẩu không khớp!"

        except:
            err_msg = "Hệ thống đang có lỗi!Vui lòng thử lại sau!"

    return render_template("layout/register.html", err_msg=err_msg, loaiKhach=loaiKhach)


@app.route("/update-khach", methods=['get', 'post'])
def update_khach():
    if session.get("khach"):
        msg = ''
    else:
        msg = 'Bạn chưa đăng nhập!!!'
    taiKhoanKhach = session.get("khach")
    khach = utils.get_BangSDT(taiKhoanKhach['khach']['id'])
    loaiKhach = utils.get_LoaiKhach()

    if request.method == 'POST':
        if khach:
            maKhach = session.get("khach")['khach']['id']
            username = request.form["username"]
            password = request.form["password"]
            maLoaiKhach = request.form["LoaiKhach"]
            CMND = request.form["CMND"]
            diaChi = request.form["DiaChi"]
            ngaySinh = request.form["NgaySinh"]
            SDT = request.form["SDT"]
            loaiSDT = request.form["LoaiSDT"]

            if username == session.get('khach')['khach']['username']:

                if utils.update_Khach(maKhach, username, password, maLoaiKhach, CMND, diaChi, ngaySinh, SDT, loaiSDT):
                    del session['khach']
                    return redirect("/dangnhap")
                msg = 'Cập nhật thất bại! Vui lòng kiểm tra lại thông tin!!!'
                return render_template("layout/update_user.html", msg=msg, khach=khach, loaiKhach=loaiKhach)
            else:
                if utils.exist_taiKhoan(username):
                    msg = "Username đã tồn tại!!! Vui lòng đổi Username khác"
                    return render_template("layout/update_user.html", msg=msg, khach=khach, loaiKhach=loaiKhach)
                else:
                    if utils.update_Khach(maKhach, username, password, maLoaiKhach, CMND, diaChi, ngaySinh, SDT,
                                          loaiSDT):
                        del session['khach']
                        return redirect("/dangnhap")
                    msg = 'Cập nhật thất bại! Vui lòng kiểm tra lại thông tin!!!'
                    return render_template("layout/update_user.html", msg=msg, khach=khach, loaiKhach=loaiKhach)

    return render_template("layout/update_user.html", msg=msg, khach=khach, loaiKhach=loaiKhach)


if __name__ == '__main__':
    app.run(debug=True)
