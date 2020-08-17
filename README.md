# NguyenThiMinhTam_18021113_Nhom5_Crawler
Thầy cô có thể xem các cột dữ liệu trực quan và nhiều hơn tại đây ạ:
www.kaggle.com/dataset/06f1da108cd20b03e757656d79499bfa65b399fdce1e05ac9ac105b952f65627

Website : Tiki.vn

(Sử dụng thêm beautifulsoup)

+Ta dùng cách kéo 1 loạt link của các sản phẩm về mà không dùng việc loang do chế độ recommend của các trang thương mại điện tử có thể dẫn đến việc sẽ lặp đi lặp lại một vài sản phẩm nhất định

-Trên trang chủ của Tiki kéo link các danh mục về lưu trong product_type.txt

-Duyệt danh sách các link đã lấy được, tiếp tục kéo link của từng sản phẩm trong mỗi thư mục lưu vào product_id.txt. Chuyển trang bằng format (page_url).

-Duyệt trang theo danh sách link đã lấy được

-Get() các trường cần tìm (chi tiết trong file code tiki.py)

+Tùy vào thời điểm mà có thể kéo về nhiều hay ít link sản phẩm, thường thì sẽ chỉ kéo được khoảng hơn 15k link

*Ghi chú: do tiki.vn hạn chế truy cập nên dẫn đến một số trường dữ liệu bị mất, em thêm vài đk if khi get(), try catch, response.status_code để tránh lỗi, hơi dài dòng, mong thầy cô bỏ qua.
