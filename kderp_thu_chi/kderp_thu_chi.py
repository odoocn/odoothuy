from openerp.osv import fields, osv
class kderp_thu_chi(osv.osv):
    _name = "kderp.thu.chi"
    _columns = {
               'ma_phieu' : fields.char("Ma Phieu"),
               'ngay_lap_phieu' : fields.date("Ngay Lap Phieu"),
               'nguoi_nop_tien' : fields.char("Nguoi Nop Tien"),
               'nguoi_nhan_tien' : fields.char("Nguoi Nhan Tien"),
               'dia_chi': fields.text("Dia Chi"),
               'so_tien': fields.float("So Tien"),
               'ly_do':fields.text("Ly Do"),
               'kem_theo':fields.char("Kem Theo")
                }
kderp_thu_chi()