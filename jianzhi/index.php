<?php  
//获取当前文件所在的绝对目录
$dir =  dirname(__FILE__);
//扫描文件夹
$file = scandir($dir);

foreach ($file as $value) {
  echo "<a href='./".$value."' download='".$value."'>$value<br/>";
  //print_r("<a download='".$value."'><br/>");
}
//显示
//echo " <pre>";
//print_r($file);

?>