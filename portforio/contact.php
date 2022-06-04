<?php
if ($_SERVER['REQUEST_METHOD'] != 'POST') {
    // POSTでのアクセスでない場合
    $name = '';
    $email = '';
    $subject = '';
    $message = '';
    $err_msg = '';
    $complete_msg = '';

} else {
    // フォームがサブミットされた場合（POST処理）
    // 入力された値を取得する
    $name = $_POST['name'];
    $email = $_POST['email'];
    $subject = $_POST['subject'];
    $message = $_POST['message'];

    // エラーメッセージ・完了メッセージの用意
    $err_msg = '';
    $complete_msg = '';

    // 空チェック
    if ($name == '' || $email == '' || $subject == '' || $message == '') {
        $err_msg = '全ての項目を入力してください。';
    }

    // エラーなし（全ての項目が入力されている）
    if ($err_msg == '') {
        $to = ''; // 管理者のメールアドレスなど送信先を指定
        $headers = "From: " . $email . "\r\n";

        // 本文の最後に名前を追加
        $message .= "\r\n\r\n" . $name;

        // メール送信
        mb_send_mail($to, $subject, $message, $headers);

        // 完了メッセージ
        $complete_msg = '送信されました！';

        // 全てクリア
        $name = '';
        $email = '';
        $subject = '';
        $message = '';
    }
}
?>


<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>お問い合わせフォーム</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP&display=swap" rel="stylesheet"> 
    <style>
        body {
            background: #f3f3f3;
            font-family: 'Noto Sans JP', sans-serif;
        }
    </style>
    </head>

    <body>
        <div class="container mt-5 pt-5">
            <div class="row">
                <div class="col-md-6 offset-md-3">
                    <h3 class="mb-5 text-center">お問い合わせフォーム</h3>
                    <form method="post">
                        <div class="mb-3">
                            <input type="text" class="form-control" name="name" placeholder="お名前" value””>
                        </div>  
                        <div class="mb-3">
                            <input type="text" class="form-control" name="email" placeholder="メールアドレス" value””>
                        </div>  
                        <div class="mb-3">
                            <input type="text" class="form-control" name="subject" placeholder="件名" value””>
                        </div>  
                        <div class="mb-4">
                            <textarea class="form-control"  name="message" rows="5" placeholder="本文" value””></textarea>
                        </div>  
                        <div class="d-grid">
                            <button type="submit" class="btn btn-success">送信</button>
                        </div>  
                    </form>
                </div>
            </div>
        </div>
    </body>
</html>