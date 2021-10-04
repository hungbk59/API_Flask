from flask import Flask, jsonify, request
import model

app = Flask(__name__)
data = model.data


# lấy dữ liệu theo từng trang
@app.route("/data/api/v1.0/page=<int:page_head>&limit=<int:page_end>", methods=["GET"])
def get_paging(page_head, page_end):
    new = data.select().limit(page_end).offset(page_head-1).dicts()
    Data = []
    for row in new:
        Data.append(row)
    return jsonify({"paging": Data})


# Tìm kiếm dữ liệu theo tiêu đề
@app.route("/data/api/v1.0/search%tieude=<string:title>", methods=["GET"])
def get_title(title):
    chek_title = "%" + title + "%"
    new = data.select().where(data.tieude ** chek_title).dicts()
    Data = []
    for row in new:
        Data.append(row)
    return jsonify({"title": Data})


# Tìm kiếm dữ liệu theo nội dung
@app.route("/data/api/v1.0/search%noidung=<string:content>", methods=["GET"])
def get_content(content):
    chek_content = "%" + content + "%"
    new = data.select().where(data.tieude ** chek_content).dicts()
    Data = []
    for row in new:
        Data.append(row)
    return jsonify({"content": Data})


# Thêm phần dữ liệu tiêu đề và nội dung vào data
@app.route("/data/api/v1.0", methods=["POST"])
def insert_data():
    check_content = data.select(data.noidung).where(data.noidung == request.form["noidung"]).count()
    # Tiêu đề có thể trùng, nội dung phải khác nhau
    if check_content == 0:
        data.insert(tieude=request.form["tieude"], noidung=request.form["noidung"]).execute()
        return jsonify({"status": 1, "message": "Insert Successfull"})
    else:
        return jsonify({"status": -1, "message": "Duplicate content"})


# Sửa đổi dữ liệu nội dung và tiêu đề
@app.route("/data/api/v1.0/update%<int:id>", methods=["PUT"])
def update_data(id):
    check_content = data.select(data.noidung).where(data.noidung == request.form["noidung"]).count()
    if check_content == 0:
        data.update(tieude=request.form["tieude"], noidung=request.form["noidung"]).where(data.STT==id).execute()
        return jsonify({"status": 1, "message": "Update Successfull"})
    else:
        return jsonify({"status": -1, "message": "Duplicate content"})


# Xóa dữ liệu theo trang
@app.route("/data/api/v1.0/delete%<int:id>", methods=["DELETE"])
def delete_data(id):
    data.delete().where(data.STT==id).execute()
    return jsonify({"status": 1, "message": "Delete Successfull"})


# Thông báo lỗi handler
@app.errorhandler(400)
def handl_400_error(_error):
    return jsonify({"status": 400, "message": "Misunderstood"})

@app.errorhandler(401)
def handl_401_error(_error):
    return jsonify({"status": 401, "message": "Unauthorised"})

@app.errorhandler(404)
def handl_404_error(_error):
    return jsonify({"status": 404, "message": "Not found"})

@app.errorhandler(500)
def handl_500_error(_error):
    return jsonify({"status": 500, "message": "Server error"})


if __name__ == '__main__':
    app.run()