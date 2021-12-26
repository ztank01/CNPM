function addToCart(MaPhong, MaLoaiPhong){
    fetch("/api/add-item-cart",{
        method: 'post',
        body:JSON.stringify({
            "MaPhong": MaPhong,
            "MaLoaiPhong": MaLoaiPhong
        }),
        headers: {
            "Content-Type":"application/json"
        }
    }).then(function(res){
        console.info(res)
        return res.json()
    }).then(function(data){
        console.info(data)

        let counter = document.getElementById("cartCounter")
        if(counter !== null)
            counter.innerText = data.total_quantity
    })
}

function updateCartItem(MaPhong, NgayBatDau, quantity){
    fetch("/api/update-cart-item",{
        method: "put",
        body:JSON.stringify({
            "MaPhong": MaPhong,
            "NgayBatDau": String(NgayBatDau),
            "quantity": parseInt(quantity)
        }),
        headers: {
            "Content-Type":"application/json"
        }
    }).then(function(res){
        return res.json()
    }).then(function(data){
        if(data.error_code == 200){
            let d = data.cart_stats
            let quantity = document.getElementById("cart-quantity")
            let amount = document.getElementById("cart-amount")
            if (quantity !== null && amount !== null){
                let d = data.cart_stats
                quantity.innerText = d.total_quantity
                amount.innerText = d.total_amount
                location.reload()
            }
        }else
            alert("Cập nhật thất bại!")
    })
}

function deleteCartItem(MaPhong){
if (confirm("Bạn có chắc chắn muốn xóa item này không?") == true){
fetch("/api/delete-cart-item/"+MaPhong,{
        method: "delete",
    }).then(function(res){
        return res.json()
    }).then(function(data){
        if(data.error_code == 200){

            let quantity = document.getElementById("cart-quantity")
            let amount = document.getElementById("cart-amount")
            if (quantity !== null && amount !== null){
                let d = data.cart_stats
                quantity.innerText = d.total_quantity
                amount.innerText = d.total_amount

                let counter = document.getElementById("cartCounter")
                if(counter !== null)
                    counter.innerText = d.total_quantity

                //location.reload()
                let row = document.getElementById("Phong" + MaPhong)
                row.style.display = "none"
            }
        }else
            alert("Xóa thất bại!")
    })
}
}

function pay(){
    if (confirm("Bạn có chắc chắn muốn đặt phòng không?") == true)
        fetch("/api/pay",{
            method: 'post'
        }).then(function(res){
            return res.json()
        }).then(function(data){
            if(data.error_code == 200)
                location.reload()
            else
                if(data.error_code == 400)
                    alert("Có phòng "+data.msg+" đã được thuê!!! Vui lòng xóa khỏi danh sách và thực hiện lại")
                else
                    alert("Thanh toán đang có lỗi!!! Vui lòng thực hiện sau")
        })
}