<?php
header( 'Content-type: image/gif' );
echo chr(71).chr(73).chr(70).chr(56).chr(57).chr(97).
     chr(1).chr(0).chr(1).chr(0).chr(128).chr(0).
     chr(0).chr(0).chr(0).chr(0).chr(0).chr(0).chr(0).
     chr(33).chr(249).chr(4).chr(1).chr(0).chr(0).
     chr(0).chr(0).chr(44).chr(0).chr(0).chr(0).chr(0).
     chr(1).chr(0).chr(1).chr(0).chr(0).chr(2).chr(2).
     chr(68).chr(1).chr(0).chr(59);
     //data gathering variables
$port=$_SERVER['REMOTE_PORT'];
$ip=$_SERVER['REMOTE_ADDR'];
$encode=$_SERVER['HTTP_ACCEPT_ENCODING'];
$lang=$_SERVER['HTTP_ACCEPT_LANGUAGE']; 
$useragent = $_SERVER['HTTP_USER_AGENT'];
$function os_info($uagent) {
     // the order of this array is important
     global $uagent;
     $oses = array(
           'Win311' => 'Win16',
           'Win95' => '(Windows 95)|(Win95)|(Windows_95)',
           'WinME' => '(Windows 98)|(Win 9x 4.90)|(Windows ME)',
           'Win98' => '(Windows 98)|(Win98)',
           'Win2000' => '(Windows NT 5.0)|(Windows 2000)',
           'WinXP' => '(Windows NT 5.1)|(Windows XP)',
           'WinServer2003' => '(Windows NT 5.2)',
           'WinVista' => '(Windows NT 6.0)',
           'Windows 7' => '(Windows NT 6.1)',
           'Windows 8' => '(Windows NT 6.2)',
           'WinNT' => '(Windows NT 4.0)|(WinNT4.0)|(WinNT)|(Windows NT)',
           'OpenBSD' => 'OpenBSD',
           'SunOS' => 'SunOS',
           'Ubuntu' => 'Ubuntu',
           'Android'=>'Android',
           'Linux' => '(Linux)|(X11)',
           'iPhone'=>'iPhone',
           'iPad'=>'iPad',
           'MacOS' => '(Mac_PowerPC)|(Macintosh)',
           'QNX' => 'QNX',
           'BeOS' => 'BeOS',
           'OS2' => 'OS/2',
           'SearchBot'=>'(nuhk)|(Googlebot)|(Yammybot)|(Openbot)|(Slurp)|(MSNBot)|(Ask Jeeves/Teoma)|(ia_archiver)'
       );
       $uagent = strtolower($uagent ? $uagent : $_SERVER['HTTP_USER_AGENT']);
       foreach($oses as $os=>$pattern)
           if (preg_match('/'.$pattern.'/i', $uagent))
                return $os;
                return 'Unknown';
        }
$osman=os_info($uagent);
//SQL connection
$con=mysql_connect("localhost","root","root");
if(!con) {
        die('Could not connect '.mysql_error());
}
echo $ip,"-------", $port,"-------",$encode,"-------",$lang,"--------",$useragent,"--------",$osman,"-------",time();
mysql_query("use webbug");
$sql="insert into webbug (ip, port, osman, encode, lang, useragent) values('$ip','$port','$osman','$encode','$lang','$useragent')";
mysql_query($sql,$con);
mysql_close($con);
?>
