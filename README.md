# cathay_data_api_flask
 
<table>
<tr>
    <td rowspan="7"> GET：<br/>
        /rent_detail<br/>
        <br/>
        Retrieves a list of rent_detail.<br/>
        每次回傳筆數最多為10筆<br/>
        <td>genderrestrict<br/>出租性別限制</td> 
    <td> <ul>
        <li>男</li>
        <li>女</li>
		</ul>
	</td>
</tr>
<tr>
    <td>region<br/>地區</td>
    <td><ul>
        <li>台北市</li>
        <li>新北市</li>
		</ul></td>
</tr>
<tr>
    <td>dialphonenum<br/>出租人連絡電話</td>
    <td><ul>
        <li>example: 02-27551006</li>
        <li>example: 0986-851-077</li>
		</ul></td>
</tr>
<tr>
    <td>userinfo<br/>出租人身分</td>
    <td> <li>屋主</li>
        <li>非屋主</li></td>
</tr>
<tr>
    <td>usergender<br/>出租人性別</td>
    <td> <ul>
        <li>男</li>
        <li>女</li>
		</ul></td>
</tr>
<tr>
    <td>userlastname<br/>出租人姓氏</td>
    <td><ul>
        <li>example: 張</li>
		</ul</td>
</tr>
<tr>
    <td>page<br/>頁數</td>
    <td><ul>
        <li>example: 1</li>
		</ul</td>
</tr>
<tr>
    <td></td>
    <td>response</td>
    <td>{
created: "2020-02-22 07:43:53", <br/>
dialPhoneNum: "0911-550-217",<br/>
genderRestrict: "",<br/>
kfCallName: "張小姐",<br/>
region: "新北市",<br/>
rent_id: "8862066",<br/>
status: "現況獨立套房",<br/>
type: "型態公寓",<br/>
updated: "2020-02-22 07:43:53",<br/>
userInfo: "張小姐（屋主聲明：仲介勿擾）"<br/>
}</td>
</tr>

</table>
