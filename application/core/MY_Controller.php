<?php 

class MY_Controller extends CI_Controller {
	public $data = array();
	function __construct() {
		parent::__construct();
		$this->data['sitename'] = 'Jamia Connect';
	}
}

?>