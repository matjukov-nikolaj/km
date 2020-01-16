<?php

/**
 * Пример простого агента
 * случайного хода
 */
class MyCoolAgent {

	// адрес сервера
	public $url;
	// пассивные действия агента (повороты-развороты, бездействие)
	public $passivMoves;
	// активные действия агента (шаг вперед, выстрел, взятие клада, бездействие)
	public $activMoves;
	// кол-во стрел агента
	public $arrowcount;
	// пещеры в которых агент побывал
	public $knowCaves = [];
	public $knownCells = array();
	/**
	 *  Конструктор
	 */
	public function __construct() {
		$this->url			 = 'https://mooped.net/local/its/index.php?module=game&action=agentaction';
		$this->passivMoves	 = ['onLeft', 'onRight', 'upSideDn', 'noAct'];
		$this->activMoves	 = ['Go', 'Shoot', 'Take', 'noAct'];
	}

	/**
	 * Метод для соединения с сервером
	 * @param int		$id			- идентификатор попытки игры
	 * @param int		$userid		- идентификатор пользователя
	 * @param string	$act		- действия агента на текущем шагу
	 *
	 * @return object	$data->text					- объект с данными
	 * 					$data->text->currentcave	- информация о текущей пещере
	 * 					$data->text->worldinfo		- информация о мире
	 * 					$data->text->iagent			- информация об агенте
	 * 					$data->text->userid			- идентификатор пользователя
	 */
	public function connect($id, $userid, $act = 'noAct noAct') {
		$ch = curl_init();

		// GET запрос указывается в строке URL
		curl_setopt($ch, CURLOPT_URL, $this->url . "&gameid=" . $id . "&userid=" . $userid . "&act=" . urlencode($act));
		curl_setopt($ch, CURLOPT_HEADER, false);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);
		curl_setopt($ch, CURLOPT_USERAGENT, 'PHP MyCoolAgent');
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
		$curl_data = curl_exec($ch);
		curl_close($ch);

		$data = json_decode($curl_data);

		if (isset($data->error) && $data->error) {
			//error_type == 'notification' пропускаем
			//это уведомления о невозможности действий^
			//нет стрел, чтобы стрелять
			//нельзя идти вперед, потому что стена
			//взять клад, поскольку его нет в пещере
			if (!isset($data->error_type)) {
				$data->error_type = 'error';
			}

			if ($data->error_type == 'error') {
				print_r($data->error);
				die;
			}
		}

		if (!is_object($data)) {
			print_r($curl_data);
			die;
		}

		return $data->text;
	}
	
	public function SelectDirection($IAdirN = 2, $newdirN = 0) 
	 {
		 if($IAdirN == $newdirN)
		 {
			 return  "noAct";
		 }
		 else
		 {
			 $dirdiff = (( $IAdirN - $newdirN) + 4) % 4; 
			 return($this->passivMoves[$dirdiff]);
		 }
	}
	
	public function FindReturndir($curdir)
	{
		$newdirN = ($this->alldirsN[$curdir] + 2) % 4;
		$newdir = $this->alldirs[$newdirN];
		return($newdir);
	}
	
	public function CaveIsOpenedByAgent($currentCave ,$destination)
	{
		foreach($this->knowCaves as $cave)
		{
			if($cave->cNum == $this->CalculateCNum($currentCave ,$destination))
			{
				return true;
			}
		}
		return false; 
	}
	
	public function CountNum($currentCave ,$dirNum)
	{
		$col = $currentCave->colN;
		$row = $currentCave->rowN;
		 switch ($dirNum) 
		{
			case 0:
				$row--;
				break;
			case 1:
				$col++;
				break;
			case 2:
				$row++;
				break;
			case 3:
				$col--;
				break;
		}
		return $row . "_" . $col;
	}
	
	public function MakingBestMoveToTable($currentCave, $possibleWays)
	{
		$bestMoveWay = array();
		foreach($possibleWays as $value)
		{
			if(in_array($this->CountNum($currentCave ,$value), $this->deprecatedCells))
			{
				if(!is_array($bestMoveWay[1]))
				{				
					$bestMoveWay[1] = array();
				}
				array_push($bestMoveWay[1], $value);
			}		 
			elseif($this->CaveIsOpenedByAgent($currentCave, $value))
			{
				if(!is_array($bestMoveWay[5]))
				{
					$bestMoveWay[5] = array();
				}
				array_push($bestMoveWay[5], $value);
			}
			else
			{
				if(!is_array($bestMoveWay[10]))
				{
					$bestMoveWay[10] = array();
				}
				array_push($bestMoveWay[10], $value);
			}
		}
		return $bestMoveWay;
	}

	/**
	 * Метод для получения хода агента (пассив. + актив. действия) из текущего состояния
	 * @param object $currentCave	- текущая пещера агента
	 *
	 * @return string			- ход агента на данной итерации
	 */
	public function chooseAct($currentCave, $IAgent) {

		//Если в текущей пещере золото
		//Взять клад
		if ($currentCave->isGold == 1) {
			return 'noAct Take';
		}
		
		$IADir = $IAgent->dir;
		$lastMove = $IAgent->choosenact;
		
		$possibleWays = (array) $currentCave->dirList;
		//убираю путь назад
		if(in_array($possibleWays[$this->FindReturndir($IADir)], $possibleWays ))
		{
			unset($possibleWays[$this->FindReturndir($IADir)]);
		}   
		$ListMoveWay = $this->MakingBestMoveToTable($currentCave, $possibleWays);
		$bestMoveWay = $ListMoveWay[max(array_keys($ListMoveWay))];
		
		//Запись в массив известных пещер текущей пещеры
		$this->knowCaves[$currentCave->cNum] = $currentCave;
		
		if($currentCave->isBones && ($this->arrowcount  == 0) && ($this->worldInfo[ismonsteralive]== 1))//нашли Кости, а стрел нет(
		{   
			echo "Монстр рядом, но стрелы закончились( Бежим! </br>";
			$nextMove = $this->alldirs[$bestMoveWay[rand(0, count($bestMoveWay) - 1)]];
			$passivAct = $this->SelectDirection($this->alldirsN[$IADir], $this->alldirsN[$nextMove]);
			$activeWay = "Go";
		}
		elseif($currentCave->isBones && ($this->arrowcount  > 0) && ($this->worldInfo[ismonsteralive]== 1))//стрелы есть)
		{		   
			echo "Здесь кости! Победим злого монстра! </br>";
			$nextMove = $this->alldirs[$bestMoveWay[rand(0, count($bestMoveWay) - 1)]];
			$passivAct = $this->SelectDirection($this->alldirsN[$IADir], $this->alldirsN[$nextMove]);
			$activeWay = "Shoot";
		}
		elseif($currentCave->isWind) // ветер
		{		   
			//если открытых клеток больше, то в оставшейся пригодной для ходьбы будет пещера, занести в deprecated  
			//выбирать ход по наилучше схеме только тогда когда кол-во возможных ходов в этом случае больше 2
			echo "Дует ветер. Бррр </br>";
			$nextMove;
			if(count($ListMoveWay[10]) > 1 )
			{
				echo "Выбираем из [10] масива. Мы молодцы </br>";
				$nextMove = $this->alldirs[$ListMoveWay[10][rand(0, count($bestMoveWay) - 1)]];
			}
			else
			{
				if(count($ListMoveWay[10]) == 1)
				{
					echo "с помощью ветра занесли яму в запрещенный массив </br>";
					array_push($this->deprecatedCells, $this->CountNum($currentCave ,$ListMoveWay[10][0]));
				}
				 echo "Выбираем из [5] масива. Мы молодцы </br>";
				$nextMove = $this->alldirs[$ListMoveWay[5][rand(0, count($bestMoveWay) - 1)]];
			}
			$passivAct = $this->SelectDirection($this->alldirsN[$IADir], $this->alldirsN[$nextMove]);
			$activeWay = "Go";
		}
		else
		{   
			echo "Угроз нет, идем куда попало) </br>";
			if($currentCave->isHole)
			{
				echo "занесли яму в запрещенный массив </br>";
				array_push($this->deprecatedCells, $currentCave->cNum);
			}
			
			$nextMove = $nextMove = $this->alldirs[$bestMoveWay[rand(0, count($bestMoveWay) - 1)]];
			$passivAct = $this->SelectDirection($this->alldirsN[$IADir], $this->alldirsN[$nextMove]);
			$activeWay = "Go";
		}
		return $passivAct . ' ' . $activeWay;
	}

	/**
	 * Метод начала работы агента
	 * @param int	$id		- идентификатор попытки игры
	 * @param int	$userid	- идентификатор пользователя
	 * @param string	$act		- действия агента на текущем шагу
	 */
	public function runAct($id, $userid, $act = 'noAct noAct') {

		$resp = $this->connect($id, $userid, $act);

		//Агент уперся в стену,
		//Не осталось стрел
		//Получение информации о мире
		if (is_null($resp)) {
			return $this->runAct($id, $userid, 'noAct noAct');
		}
		if (!is_object($resp)) {
			print_r($resp);
			die;
		}

		//Данные для более 'умных' агентов
		$this->arrowcount		 = $resp->iagent->arrowcount;
		$this->worldInfo		 = (array) $resp->worldinfo;
		$this->IAStateUtilities	 = (array) $resp->iagent->IAStateUtilities;

		//Если золото не найдено
		//Выбор и выполнение следующего хода агента
		if (isset($resp->worldinfo->isgoldfinded) && $resp->worldinfo->isgoldfinded == 0) {
			$newAct = $this->chooseAct($resp->currentcave, $resp->iagent);
			return $this->runAct($id, $userid, $newAct);
		}
		else {
			print_r($resp);
			print_r('Золото найдено');
			die;
		}
	}

}

//Параметры: идентификатор игры и идентифкатор пользователя


$id	= null;
if (isset($_GET['id']))
	$id = filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT);
elseif (isset($_POST['id']))
	$id = filter_input(INPUT_POST, 'id', FILTER_VALIDATE_INT);

$userid	= null;
if (isset($_GET['userid']))
	$userid = filter_input(INPUT_GET, 'userid', FILTER_VALIDATE_INT);
elseif (isset($_POST['userid']))
	$userid = filter_input(INPUT_POST, 'userid', FILTER_VALIDATE_INT);


//Проверка на наличие параметров
if (empty($id) || is_null($id)) {
	print_r('Invalid id param');
	die;
}
if (empty($userid) || is_null($userid)) {
	print_r('Invalid userid param');
	die;
}

//Инициализация агента
$myAgent = new MyCoolAgent();
//Запуск работы агента
$myAgent->runAct($id, $userid); // передаем id игры и userid
//Запускать так, например:
//http://localhost/random_agent.php?id=41&userid=2
