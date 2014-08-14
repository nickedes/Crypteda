<!DOCTYPE html>
<html>
<head>
	<title>Jamia Connect</title>
	<style type="text/css">
		body {
	      text-align: center;
	      /*background: url("http://dash.ga.co/assets/anna-bg.png");*/
	      background: url("/jmiconnect/assets/images/bg.png");
	      background-size: cover;
	      background-position: center;
	      color: white;
	      font-family: helvetica;
	      height: 100%;
    	}
    	p {
    		font-size: 20px;
    	}
    	input {
    		border: 0;
    		padding: 10px;
    		margin-left: 5px;
    	}
    	input[type="submit"] {
    		background: red;
    		color: white;
    	}
    	.center-align {
    		position: relative;
			top: 50%;
			-webkit-transform: translateY(-50%);
			-ms-transform: translateY(-50%);
			transform: translateY(100%);
    	}
	</style>
</head>
<body>
	<div class="center-align">
		<h1>Welcome to Jamia Connect</h1>
		<p>A place to get in touch, collaborate and share with JMI'tes</p>
		<form>
			<input type="email" placeholder="Email" name="email">
			<input type="password" placeholder="Password" name="password">
			<input type="submit" name="submit" value="Login">
		</form>
	</div>
</body>
</html>