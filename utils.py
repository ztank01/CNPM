import datetime
import hashlib

from flask import session
from flask_login import current_user
from sqlalchemy import exists
from sqlalchemy import func

from my_app import db, app
from my_app.models import ChiTietThue, Phong, LoaiPhong, TaiKhoanKhach, HoaDon, Khach, LoaiKhach, \
    SDT, ThongSoQuyDinh


def get_tongtien(from_date=None, to_date=None):
    bcao = db.session.query(Phong.MaLoaiPhong, func.sum(HoaDon.ThanhTien))

    if from_date:
        bcao = bcao.filter(HoaDon.NgayTraPhong.__ge__(from_date))
    if to_date:
        bcao = bcao.filter(HoaDon.NgayTraPhong.__le__(to_date))

    return bcao.join(ChiTietThue, ChiTietThue.MaPhong == Phong.MaPhong).join(HoaDon,
                                                                             HoaDon.MaHopDong == ChiTietThue.MaHopDong).group_by(
        Phong.MaLoaiPhong).all()


def get_tongtile(from_date=None, to_date=None):
    tile = db.session.query(HoaDon.MaHopDong, func.sum(HoaDon.ThanhTien))

    if from_date:
        tile = tile.filter(HoaDon.NgayTraPhong.__ge__(from_date))
    if to_date:
        tile = tile.filter(HoaDon.NgayTraPhong.__le__(to_date))

    return tile.all()


def get_phongdatt(from_date=None, to_date=None):
    phong = db.session.query(ChiTietThue.MaPhong, ChiTietThue.SoNgayODuKien).filter(
        ~exists().where(ChiTietThue.MaHopDong == HoaDon.MaHopDong))
    if from_date:
        phong = phong.filter(ChiTietThue.NgayBatDau.__ge__(from_date))
    if to_date:
        phong = phong.filter(ChiTietThue.NgayBatDau.__le__(to_date))
    return phong.all()


def get_phongchuatt(from_date=None, to_date=None):
    phong = db.session.query(ChiTietThue, HoaDon).filter(ChiTietThue.MaHopDong == HoaDon.MaHopDong)
    if from_date:
        phong = phong.filter(ChiTietThue.NgayBatDau.__ge__(from_date))
    if to_date:
        phong = phong.filter(ChiTietThue.NgayBatDau.__le__(to_date))
    return phong.all()


def get_songaychuatt(ngaythue, ngaytra):
    return (ngaytra - ngaythue).days


def get_laphoadon(mahopdong=None):
    hopdong = db.session.query(Khach.MaLoaiKhach, Khach.DiaChi, ChiTietThue.MaHopDong, ChiTietThue.MaPhong,
                               ChiTietThue.SoNgayODuKien, LoaiPhong.DonGia).filter(
        ~exists().where(ChiTietThue.MaHopDong == HoaDon.MaHopDong))
    if mahopdong:
        hopdong = hopdong.filter(ChiTietThue.MaHopDong == mahopdong)
    return hopdong.join(Khach, Khach.MaKhach == ChiTietThue.MaKhach).join(Phong,
                                                                          Phong.MaPhong == ChiTietThue.MaPhong).join(
        LoaiPhong, LoaiPhong.MaLoaiPhong == Phong.MaLoaiPhong).all()


def getUserName():
    return TaiKhoanKhach.query.filter(TaiKhoanKhach.MaKhach == current_user.get_id()).first().username


def getAllRoomByUserID():
    # current_user.get_id()
    sq = db.session.query(HoaDon).filter().subquery()
    return db.session.query(ChiTietThue, Phong, LoaiPhong).filter(ChiTietThue.MaKhach == current_user.get_id(),
                                                                  ~exists().where(
                                                                      sq.c.MaHopDong == ChiTietThue.MaHopDong)).join(
        Phong, Phong.MaPhong == ChiTietThue.MaPhong).join(LoaiPhong, Phong.MaLoaiPhong == LoaiPhong.MaLoaiPhong).all()


def price(NgayBatDau, DonGia):
    price1room = (datetime.datetime.now() - NgayBatDau).days * int(DonGia) * 1000
    return price1room


def soNgayO(NgayBatDau):
    soNgay = (datetime.datetime.now() - NgayBatDau).days
    return soNgay


def totalPrice(rooms):
    priceAllRooms = 0
    for row in rooms:
        priceAllRooms = priceAllRooms + int(row[4])
    return priceAllRooms


def get_songay(from_date=None, to_date=None):
    songay = db.session.query(ChiTietThue.MaPhong, func.sum(ChiTietThue.SoNgayODuKien))
    if from_date:
        songay = songay.filter(ChiTietThue.NgayBatDau.__ge__(from_date))
    if to_date:
        songay = songay.filter(ChiTietThue.NgayBatDau.__le__(to_date))

    return songay.group_by(ChiTietThue.MaPhong).all()


def get_songaytile(from_date=None, to_date=None):
    songay = db.session.query(ChiTietThue.MaPhong, func.sum(ChiTietThue.SoNgayODuKien))
    if from_date:
        songay = songay.filter(ChiTietThue.NgayBatDau.__ge__(from_date))
    if to_date:
        songay = songay.filter(ChiTietThue.NgayBatDau.__le__(to_date))

    return songay.all()


def get_LoaiKhach(MaLoaiKhach=None):
    loaiKhach = LoaiKhach.query

    if MaLoaiKhach:
        loaiKhach = loaiKhach.filter(LoaiKhach.LoaiKhach == MaLoaiKhach)

    return loaiKhach.all()


def get_LoaiPhong(MaLoaiPhong=None):
    loaiPhong = LoaiPhong.query

    if MaLoaiPhong:
        loaiPhong = loaiPhong.filter(LoaiPhong.MaLoaiPhong == MaLoaiPhong)

    return loaiPhong.all()


def get_Phong(kw=None, MaLoaiPhong=None, page=None):
    phong = Phong.query.join(LoaiPhong).outerjoin(ChiTietThue, HoaDon)

    if kw:
        phong = phong.filter(Phong.MaPhong.contains(kw))

    if MaLoaiPhong:
        phong = phong.filter(Phong.MaLoaiPhong == MaLoaiPhong)

    if page:
        size = app.config["PAGE_SIZE"]
        start = (page - 1) * size
        end = start + size

        return phong.all()[start:end]

    return phong.all()


def get_PhongTrong(kw=None, MaLoaiPhong=None, page=None):
    phong = Phong.query

    if kw:
        phong = phong.filter(Phong.MaPhong.contains(kw))

    if MaLoaiPhong:
        phong = phong.filter(Phong.MaLoaiPhong == MaLoaiPhong)

    if page:
        size = app.config["PAGE_SIZE"]
        start = (page - 1) * size
        end = start + size

        return phong.filter(Phong.TinhTrang == 'FR').all()[start:end]

    return phong.all()


def get_BangSDT(maKhach):
    bangSDT = db.session.query(Khach).join(SDT, Khach.SDT).join(LoaiKhach).filter(Khach.MaKhach == maKhach).all()
    return bangSDT


def update_Khach(maKhach, username=None, password=None, maLoaiKhach=None, CMND=None, diaChi=None, ngaySinh=None,
                 soDT=None,
                 loaiSDT=None):
    khach = db.session.query(Khach).join(SDT, Khach.SDT).filter(Khach.MaKhach == maKhach).all()[0]
    khach.MaLoaiKhach = maLoaiKhach
    khach.CMND = CMND
    khach.DiaChi = diaChi
    khach.NgaySinh = ngaySinh
    khach.SDT[0].SDT = soDT
    khach.SDT[0].LoaiSDT = loaiSDT

    taiKhoanKhach = db.session.query(TaiKhoanKhach).get(maKhach)
    taiKhoanKhach.username = username
    if password != session.get('khach')['khach']['password']:
        password = str(hashlib.md5(password.encode("utf-8")).digest())
    taiKhoanKhach.password = password

    try:
        db.session.commit()
        return True
    except:
        return False


def kiemTraPhongTrong(maPhong):
    phong = db.session.query(Phong).get(maPhong)
    if phong.TinhTrang == 'IU':
        return False
    return True


def update_TrangThaiPhong(maPhong):
    phong = db.session.query(Phong).get(maPhong)
    try:
        phong.TinhTrang = 'IU'
        return True
    except Exception as ex:
        print("ERROR: " + str(ex))
        return False


def add_HoaDon_ChiTietThue(cart):
    if cart:
        print(session.get('khach')['khach']['username'])
        username = session.get('khach')['khach']['username']
        password = session.get('khach')['khach']['password']
        user = TaiKhoanKhach.query.filter(TaiKhoanKhach.username == username,
                                          TaiKhoanKhach.password == password).first()
        print(user.MaKhach)
        try:
            for p in cart.values():
                maPhong = p["MaPhong"]
                ngayBatDau = p["NgayBatDau"]
                soNgayODuKien = p["quantity"]
                chiTietThue = ChiTietThue(MaPhong=maPhong, MaKhach=user.MaKhach, NgayBatDau=ngayBatDau,
                                          SoNgayODuKien=soNgayODuKien)
                db.session.add(chiTietThue)

                ngayTraPhong = datetime.date(*[int(i) for i in str(ngayBatDau).split("-")]) + datetime.timedelta(
                    days=soNgayODuKien)
                thanhTien = p["DonGia"] * p["quantity"]
                hoaDon = HoaDon(ChiTietThue=chiTietThue, NgayTraPhong=ngayTraPhong, ThanhTien=thanhTien)
                db.session.add(hoaDon)
                if not update_TrangThaiPhong(maPhong):
                    return False

            db.session.commit()
            return True
        except Exception as ex:
            print("HOA DON ERROR: " + str(ex))

    return False


def count_Phong(MaLoaiPhong=None, TinhTrang=None, kw=None):
    phong = Phong.query

    if TinhTrang:
        phong = phong.filter(Phong.TinhTrang == TinhTrang)

    if MaLoaiPhong:
        phong = phong.filter(Phong.MaLoaiPhong == MaLoaiPhong)

    if kw:
        phong = phong.filter(Phong.MaPhong.contains(kw))
    return phong.count()


def cart_stats(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for p in cart.values():
            if session.get('khach'):
                loaiKhach = Khach.query.join(LoaiKhach).filter(Khach.MaKhach==session.get('khach')['khach']['id']).all()
                if loaiKhach:
                    if loaiKhach[0].LoaiKhach.LoaiKhach == 'NuocNgoai':
                        total_amount += p["DonGia"] * p["quantity"] * ThongSoQuyDinh.query.all()[0].GiaTri
                    else:
                        total_amount += p["DonGia"] * p["quantity"]
            else:
                total_amount += p["DonGia"] * p["quantity"]

            total_quantity += 1

    return {
        "total_quantity": total_quantity,
        "total_amount": total_amount
    }


def add_Khach(username=None, password=None, maLoaiKhach=None, CMND=None, diaChi=None, ngaySinh=None, soDT=None,
              loaiSDT=None):
    sdt = SDT(LoaiSDT=loaiSDT, SDT=soDT)
    db.session.add(sdt)

    khach = Khach(MaLoaiKhach=maLoaiKhach, CMND=CMND, DiaChi=diaChi, NgaySinh=ngaySinh)
    khach.SDT.append(sdt)
    db.session.add(khach)

    password = str(hashlib.md5(password.encode("utf-8")).digest())
    taiKhoanKhach = TaiKhoanKhach(Khach_TaiKhoan=khach, username=username, password=password)
    db.session.add(taiKhoanKhach)

    try:
        db.session.commit()
        return True
    except:
        return False


def exist_taiKhoan(username):
    taiKhoanKhach = TaiKhoanKhach.query.filter(TaiKhoanKhach.username == username).all()
    if taiKhoanKhach:
        return True
    return False


if __name__ == '__main__':
    rooms = getAllRoomByUserID()
    new_list = []
    for row in rooms:
        new_row = list(row)
        new_row.append(soNgayO(row[0].NgayBatDau))
        new_row.append(price(row[0].NgayBatDau, row[2].DonGia))
        new_list.append(tuple(new_row))
        print(row[0].MaHopDong)
