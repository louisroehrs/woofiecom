#!usr/bin/perl

print "################################## \n";
print "Starting Klissarian Web game engine \n";
print "################################## \n"; 

##################################
# main.cgi.
# Creation date :  1/30/98
# Last modified : 3/12/98
# by Sera Linardi
# Klissarian Web
# Main.cgi starts a new game and/or execute a 
# turn on an continuing game.
#################################

########################################################
# declare local variables
#
$host = 'localhost';
$database = 'jubal';
$GN = 0;
$SN = 0;
@Player = ();
@Planet = ();

#################################

####USE DECLARATION
use CGI;
use CGI qw(:cgi-lib);
use CGI qw(:standard);
use Text::Boilerplate;
use AutoLoader;
use KwebObject();
use Player();
use System();
use Planet();
use DBI;

# connect with the dB "jubal"
#
$dbh = DBI->connect("DBI:mSQL:$database:$host",undef,undef)
    || die "not ok connect: ";

my $q0 = "SELECT DISTINCT GameNo FROM PlayerSignup where Active=1";

my $sth0 = $dbh->prepare($q0);
$sth0->execute;

while( @game_array = $sth0->fetchrow_array ) {
     my $game = $game_array[0];
     print "Checking on status of Game $game. \n";


#####################################

###delete this in real game, now only testing gameNo 2070
     if ($game == 2070) {
       print "Executing turn for Game $game.\n";  
       execute_turn_for_game($game);
     }
#####################################
}

  $sth0->finish;

  # disconnect with the DB "jubal"
  my $rc = $dbh->disconnect();


##################################

### GENERAL PURPOSE SUBS
###operate on DB once, returns nothing.
sub operate_on_DB {
       my ($query) = @_;
       ## print "query : $query\n";
       my $sth = $dbh->prepare($query);
       $sth->execute;
       $sth->finish;
}

###return number of rows that DB returns
sub returnDBrow {
       my ($query) = @_;
       my $sth = $dbh->prepare($query);
       ## print "query : $query \n"; 
       $sth->execute;
       my $row = $sth->rows;
       ## print "num row : $row \n";
       $sth->finish;
       return $row;
}

sub findIndex {
## all references to table Player changed to PlayerStat. RKS.
    my ($table, $key) = @_;
    if ($table eq '' || $key eq '') {return 0;}
    my $q ;
    if ($table eq 'PlayerStat') {
       $q= "SELECT DISTINCT PlayerNo FROM PlayerStat WHERE GameNo=".
	$GN." AND FactionName='" .$key. "'"; 
    } elsif ($table eq 'StartPlanets') {
	$q = "SELECT DISTINCT SysNo FROM StartPlanets WHERE Star='".
	$key."'";
    } else {    
       $q= "SELECT DISTINCT SysNo FROM ".$table." WHERE GameNo=".
	$GN." AND Star='".$key. "'";
   }
    my $sth= $dbh->prepare($q);
    $sth->execute();
    my @sysno = $sth->fetchrow_array;
    my $no = $sysno[0];
    $sth->finish();
    return $no;
}

sub findString {
    my ($table, $key) = @_;
    if ($table eq '' || $key == 0) {return '';}
    my $q ;
    if ($table eq 'PlayerStat') {
       $q= "SELECT DISTINCT FactionName FROM PlayerStat WHERE GameNo=".
	   $GN." AND PlayerNo=" .$key. "";
   } elsif ($table eq 'StartPlanets') {
        $q = "SELECT DISTINCT Star FROM StartPlanets WHERE SysNo=".
	   $key;
   } else {
        $q= "SELECT DISTINCT Star FROM ".$table.
	   " WHERE GameNo=".$GN." AND SysNo=".$key. "";
   } 
    my $sth= $dbh->prepare($q);
    $sth->execute();
    my @names = $sth->fetchrow_array;
    my $name = $names[0];
    $sth->finish();
    return $name;
}

     
##################################
### sub to start a new game

## Prepare database for a new game.
## Get 12 names of player that does not have a game number
## assigned to them and assign them $new_game_num
## Start out these players with equally equipped planets.

## sub startGame {
  ## my ($game_number) = @_;
  ## ## set the global var to the currently processed game.
  ## $GN = $game_number;
  ## # needs to be included to init StartPlanet table for a new game
  ## system ("perl initStartPlanets.pl");
  ## my @list_of_races  = ();
  ## my $i=0;
  ## $SN = 0;
  ## my $q = "INSERT INTO GameStatus Values (".$GN.",0)";
  ## operate_on_DB($q);
  ## my $q2 = "SELECT * FROM PlayerStat where GameNo=" . $game_number;
  ## my $sth2 = $dbh->prepare($q2);
  ## $sth2->execute;
  ## while ($Player_ref = $sth2->fetchrow_hashref ) {
             ## my $player_no = $Player_ref->{'PlayerNo'};
	     ## my $name = $Player_ref->{'FactionName'};
	     ## my $race = $Player_ref->{'Race'};
             ## my $first = 1;
             ## foreach my $list_of_race (@list_of_races) {
                 ## if ($list_of_race eq $race ) { $first=0; break; };
             ## }             
             ## createStartPlanet($name, $player_no, $race, $first);
             ## $list_of_races[$i]=$race;
             ## $i++;
  ## }
  ## #print @list_of_races;
  ## $sth2->finish;
  ## #create entries of uninhabited planet
  ## createOtherPlanetEntries();
  ## #System table is just a table of distances 
  ## createSystem();  
  ## my $q = "UPDATE GameStatus SET LastShipNo=".$SN." WHERE GameNo=".$GN;
  ## operate_on_DB($q);
 ##  
## }

## Determine which planet which Player starts with, 
## according to their race. Query the dB for available planets.
## Create $Player's starting Planet with 
## max 4 mines, 4mines, 20 industry, 10 shock troops
## sub createStartPlanet {
       ## my ($name, $owner_no, $race, $first) = @_;
       ## my @eligible_planets = ();
       ## my $i = 0;       my $system = '';    my $orbit = 0; my $no=0;
       ## if ($first ) {
            ## ($system, $orbit) = getFirstPlanet($race);
       ## } else {    
            ## $q3 = "SELECT * FROM StartPlanets where NativeRace='" . $race . "' AND Can_Settle=1 AND Is_Settled=0";
            ## $sth3 = $dbh->prepare($q3);
            ## $sth3->execute;
            ## while ( $planet_ref = $sth3->fetchrow_hashref ){            
               ## $eligible_planets[$i]{'Star'} = $planet_ref->{'Star'};
               ## $eligible_planets[$i]{'Orbit'} = $planet_ref->{'Orbit'};
	      ## $i++;
	    ## }
            ## ### get a random index 
            ## my $planet_index = rand($i);
            ## $system = $eligible_planets[$planet_index]{'Star'};
            ## $orbit = $eligible_planets[$planet_index]{'Orbit'};
            ## $sth3->finish;
      ## } 
      ## my $no = findIndex('StartPlanets', $system);
      ## ### change $IsSettled to 1 at initialization table. 
      ## my $q4 = "UPDATE StartPlanets SET Is_Settled=1 WHERE Star='" .
		## ## $system . "' AND Orbit=" . $orbit; 
      ## operate_on_DB($q4);
     ## ### write to individual Planet entry
     ## ### Maintanance here is precalc to 5 from the ships we start them
     ## ### out with (1 battleship, 3 frigates)
      ## $q5 = "INSERT INTO Planet VALUES (".$GN.",".$no.",'" . $system . "'," .
	## $orbit . ",1,0,'',".$owner_no.",'".$name."',20,4,4,0,0,0,0,0)";
      ## operate_on_DB($q5);
       ## print "Assigned $system, $orbit to $name. \n";
      ## addStartingShips($no, $system, $orbit, $owner_no, $name); 
 ## }

## sub addStartingShips {
    ## my ($sysno, $sysname, $orbit, $owner_no, $owner_name) = @_;
    ## addShip ($sysno, $orbit, 'Battleship', $owner_no, $owner_no, 1,0);
    ## addShip ($sysno, $orbit, 'Frigate', $owner_no, $owner_no, 3,0);
   ##  
## } 
## 
## ## Gives the first of a race a predetermined starting point
## sub getFirstPlanet {
       ## my ($race) = @_;
       ## my @planet = ();
       ## if ($race eq 'Human') { $planet[0]='Sol'; $planet[1]=3;}
       ## elsif ($race eq 'Klissarian') { $planet[0]='Chara'; $planet[1]=3;} 
       ## elsif ($race eq 'Ngdomi') { $planet[0]='70 Ophiuchi'; $planet[1]=2;}
       ## elsif ($race eq 'Poxmec') { $planet[0]='Sigma Draconis'; $planet[1]=4;}
       ## else { die "$race is not a known race."; }
       ## return @planet;
 ## }
## 
## ## Create a Planet entry in the DB for the rest of the uninhibited planets
## sub createOtherPlanetEntries{
      ## my $q6 =  "SELECT * FROM StartPlanets where Is_Settled=0";
      ## my $sth6 = $dbh->prepare($q6);
      ## $sth6->execute;
      ## while ( $planet_ref = $sth6->fetchrow_hashref ){
	  ## $sysno = $planet_ref->{'SysNo'};
          ## $system = $planet_ref->{'Star'};
          ## $orbit = $planet_ref->{'Orbit'};  
          ## $can_settle = $planet_ref->{'Can_Settle'};
          ## my $max_mines = 0;
          ## ## if ($can_settle) {$max_mines = int(rand(4)); $max_mines+=1; }
           ## my $q7 = "INSERT INTO Planet VALUES (" . $GN . "," .$sysno. ",'" . $system . "'," . $orbit . "," .$can_settle. ",0,'',0,'',0,0," . $max_mines . ",0,0,0,0,0)";
	  ## operate_on_DB($q7);
       ## }
       ## $sth6->finish;
## }

## sub createSystem {
    ## my @star_array=();
    ## my $q =  "SELECT DISTINCT Star FROM StartPlanets";
    ## my $sth = $dbh->prepare($q);
    ## $sth->execute;
    ## while ( $star = $sth->fetchrow_array ){
         ## my $q60 = "SELECT * FROM StartPlanets where Star='".$star."'";
         ## my $sth60 = $dbh->prepare($q60);
         ## $sth60->execute;
         ## my $xyz = $sth60->fetchrow_hashref;
         ## my $x = $xyz->{'x'};
         ## my $y = $xyz->{'y'};
         ## my $z = $xyz->{'z'};       
         ## my $qq = "INSERT INTO System VALUES (".$GN.",'".$star."',".$x.",".$y.",".$z.")";
         ## operate_on_DB($qq);    
         ## $sth60->finish;
     ## }
    ## $sth->finish;
## }
#################################################################
##Completely Bug Free until here (as far as I can test :-) 03/12/98         
## Wrong. RKS. 4/10/98
#################################################################
### general subroutines to load every turn

sub execute_turn_for_game {
    my ($game_number) = @_;
    ## set the global var to the currently processed game.
    $GN = $game_number;
    loadPlayers(); 
    loadPlanets();  

# remove for real game...left by Sera, so be careful
# $Planet->[1][3]->maxMines();       

    processAll();
}

### load all the Players in a game
sub loadPlayers {
    my $q = "SELECT * FROM PlayerStat where GameNo=" . $GN;
    my $sth = $dbh->prepare($q);
    $sth->execute;
    while ( $player_ref = $sth->fetchrow_hashref ){
        my $no = $player_ref->{'PlayerNo'};
        my $name = $player_ref->{'FactionName'};
        my $race = $player_ref->{'Race'};
        my $attack = $player_ref->{'Attack'};
        my $defense = $player_ref->{'Defense'};
        my $infantry = $player_ref->{'Infantry'};
        my $sensor = $player_ref->{'Sensor'};
        my $industry = $player_ref->{'Industry'};
        my $mining = $player_ref->{'Mining'};
        my $esp = $player_ref->{'Espionage'};
        my $tactics = $player_ref->{'Tactics'};
        $Player[$no] = Player->new($name, $race, 
		$attack, $defense, $infantry, $sensor, 
		$industry, $mining, $esp, $tactics);
    }
    $sth->finish;
}


### Create all Planets 
##	added $engagedBases var to track bases which have already attacked
##	begins at '0' each turn. RKS
##
sub loadPlanets {     
    my $q = "SELECT * FROM Planet where GameNo=" . $GN;
    my $sth = $dbh->prepare($q);
    $sth->execute;
    while ( $planet_ref = $sth->fetchrow_hashref ){
        my $systemno = $planet_ref->{'SysNo'};
	my $system = $planet_ref->{'Star'};
	my $orbit = $planet_ref->{'Orbit'};
        my $can_set = $planet_ref->{'Can_Settle'};
        my $ownerno = $planet_ref->{'OwnerNo'};
        my $ownerName = $planet_ref->{'OwnerFactionName'};
        my $fac = $planet_ref->{'TotalFactories'};
        my $mines = $planet_ref->{'TotalMines'};
        my $maxmines = $planet_ref->{'MaxMines'};
        my $rawmat = $planet_ref->{'RawMaterial'};
        my $bases = $planet_ref->{'NoBases'};
        my $maint = $planet_ref->{'LastTurnMaint'};
        my $st = $planet_ref->{'Troops'};
        my $s = $planet_ref->{'SecurityLevel'};
        my $eB = 0;
        $Planet->[$systemno][$orbit] = Planet->new($system, 
		$orbit, $can_set, $ownerno, $ownerName, 
		$fac, $mines, $maxmines, $rawmat, $bases, 
		$st, $s, $eB, $maint);
        ## if planet has owner, we automatically refill stockpile
        if ($ownerno) {
           my $mining = $Player[$ownerno]->mining();
           $Planet->[$systemno][$orbit]->mine($mining);
         } 
	## OK. RKS.
	## print $Planet->[$systemno][$orbit]->name() . "\n";
    } 
    $sth->finish;
}


###########################################
### Process all of orders.


### I think this would be random enough. 
### First we sort for order ### type
#
sub processAll {
   print "###################################\n";
   print "Processing orders for $GN this turn \n";
   print "####################################\n";  
   		################
   		##  DIRECT TESTS
   		################

   print "\nUpdating ship movements. Subtracting 1 from all Ships\n";
   print "with a TurnTillActive > 0\n";
   updateShip($GN);

# my @orderTypes = ('attack', 'transport', 'move', 
#	'unload', 'build', 'spy', 'security', 'ally', 'unally', 'homeport');
#####################################
##   used for debugging by sera/RKS
   ## my @orderTypes = ('ally'); 	## done. tested. RKS
   ## my @orderTypes = ('unally'); 	## done. tested. RKS 
   ## my @orderTypes = ('security'); 	## need to do cost for order. RKS
				  	## done. needs thorough testing. RKS
   ## my @orderTypes = ('spy'); 	## done. tested. RKS 
   ## my @orderTypes = ('contract'); 	## done. tested. RKS 
   ## my @orderTypes = ('build'); 	## done. tested. RKS 
   ## my @orderTypes = ('build','transport', 'unload'); ## unload. Louis.	
   ## my @orderTypes = ('move'); 	## done. tested. RKS

   my @orderTypes = ('attack'); 	## testing. RKS

   ## my @orderTypes = ('transport', 'move', 'build'); 	## done. tested. RKS 
   ## my @orderTypes = ('move', 'transport','contract','build','ally','unally','security','spy'); 
#####################################

   foreach $orderType (@orderTypes) {                
      print "Checking $orderType \n";
      my $q10 = "SELECT * FROM Planet where GameNo= " . $GN;
      my $sth10 = $dbh->prepare($q10);
      $sth10->execute;

	# planet_ref is global var
      while ( $planet_ref = $sth10->fetchrow_hashref ){
	   ##
	   ## $sys is System char
	   ##
          $sys= $planet_ref->{'Star'};
          $orbit = $planet_ref->{'Orbit'};
	  
	  print "\nsystem: $sys orbit: $orbit <-> ";
          if ($orderType eq 'attack') {
                attack($sys, $orbit);
	  }

          my $q11 = "SELECT * FROM Orders where GameNo= " .$GN
		. " AND OrderType='" .$orderType. "' AND System='" 
		.$sys. "' AND Orbit=" .$orbit;
          my $sth11 = $dbh->prepare($q11);
          $sth11->execute;
          while ( $order_ref = $sth11->fetchrow_hashref ){
	   	##
		## $system is SystemNo
	   	##
	       print "\n\n";
	       my $system = findIndex('Planet', $sys);
               if ($orderType eq 'transport') { 
	           transport($order_ref, $system, $orbit);
               } 
	       elsif   ($orderType eq 'move') {
                   move($order_ref, $sys, $orbit);
               } 
	       elsif   ($orderType eq 'unload') {
                   unload($order_ref, $system, $orbit);
               } 
	       elsif   ($orderType eq 'build') {
		   ## not necessary. duplicate of above decl. 
		   ## left by sera. RKS.
                   ## my $system = findIndex('Planet', $sys);
                   build($order_ref, $system, $orbit);
               } 
	       elsif ($orderType eq 'contract') {
                   ## my $system = findIndex ('Planet', $sys);
                   build($order_ref, $system, $orbit);
               } 
	       elsif   ($orderType eq 'spy') {
                   spy($order_ref, $system, $orbit);   
               } 
	       elsif   ($orderType eq 'security') {
                   security($order_ref, $system, $orbit);   
 	       } 
	       elsif   ($orderType eq 'ally') {
                   ally( $order_ref );
               } 
	       elsif   ($orderType eq 'unally') {
		   unally($order_ref);
               } 
	       else {
#################################################
	## needs to be added. 
	## homeport($order_ref);
#################################################
		  ;
               }
           }
           $sth11->finish;

		## process_overrun_table not coded. RKS
		## found it in #text# pseudo-code. not transferred.
		## added to main.cgi. RKS

           if ($orderType eq 'attack') {
	      process_overrun_table($system, $orbit); 
           }
      } 	## end while $sth10
      $sth10->finish;

  }		## end foreach orderType

## used for debugging
## moving ship 5 light years is done in maintain()
## next two lines left commented by sera. RKS.
#  maintanance();
  writeToDatabase();

#################################################
## remove for real game to allow new orders
       $q12 = "DELETE FROM Orders where GameNo=" . $GN;
       # operate_on_DB($q12);
#################################################
}


sub transport {
	## $system is SystemNo
	## changed system to systemNo. RKS
  my ($order_ref, $systemNo, $orbit) = @_;
  my $name = $order_ref->{'FactionName'};
  my $numload = $order_ref->{'NumObject'};
  my $load_type = $order_ref->{'ObjectType'};
  my $system_des = $order_ref->{'SystemDes'};
  my $orbit_des = $order_ref->{'OrbitDes'};
  my $maxLoad = 5;
  my $shipno = 0; 
  my $rmload = 0;
  my $facload = 0; 
  my $stload = 0;
  my $currentLoad = 0;
  my $room_for_load = 0;
  my $stdquery = "";
  my $totalrmload = 0;
  my $totalfacload = 0;
  my $totalstload = 0;
    
  print "transporting: sytemno: $systemNo orbit: $orbit for faction: ";
  print "$order_ref->{'FactionName'} to systemDes: $order_ref->{'SystemDes'} \n";
  print "orbit: $orbit_des how many: $numload what: $load_type \n";

	# ...->owner returns Planet Owner Number
	# verifies goods from planet belong to this player
  return unless ($Planet->[$systemNo][$orbit]->owner() == 
    				findIndex('PlayerStat',$name));

	## ->enough not written be sera.RKS. 
	## enough is verifying enough space on all
	## transports at this star/orbit to transport goods
 	### transport order fail unless there's enough transports.RKS

  return unless enough($systemNo, $orbit, $name, $load_type, $numload);
	
	## floundering attempts to code enough. RKS
	## ($Planet->[$systemNo][$orbit]->enough($raw_mat, $troops, $fac));
	## ($Planet->[$systemNo][$orbit]->enough($systemNo, 
        ##			$orbit, $name, $numload);

	## system_des is CHAR, calcturns must pass INT. RKS
  	## my $distance = calcturns($system_des,$systemNo);
  my $distance = calcturns(findIndex('Planet',$system_des), $systemNo);

  print "distance to  destination: $distance\n";

  $q13 = "SELECT * FROM Ship where GameNo= " . $GN . " AND OwnerFactionName ='" 
	. $name . "'  AND ShipType='Transport' AND SysNo=" 
	. $systemNo . " AND Orbit=" . $orbit 
	. " AND TurnTillActive = 0 ORDER BY ShipNo";

		## removed line from code. left by sera. 
		## not needed here. covered in code below. RKS
		## AND ( ( Ship.RawMat + Ship.Fac + Ship.Troops) < 5)";
  $sth13 = $dbh->prepare($q13);
  $sth13->execute;

	## should this be an &&. I beleve so. changed. RKS.
  	## while ($ship_ref = $sth13->fetchrow_hashref || $numload > 0) 
  while ( ($ship_ref = $sth13->fetchrow_hashref) && $numload > 0) {
      $shipno = $ship_ref->{'ShipNo'};
      $rmload = $ship_ref->{'RawMat'};
      $facload = $ship_ref->{'Fac'};
      $stload = $ship_ref->{'Troops'};
      print "shipno: $shipno rmload: $rmload ";
      print "facload: $facload stload: $stload \n";

      	 ### verify the ship has enough room to load it
	 ### if enough room, load ship, else, go to next ship
      $currentLoad = $rmload + $facload + $stload;
      print "transport ship current load: $currentLoad < maxload: $maxLoad\n";

      if ( $currentLoad < $maxLoad ) {

      	 ###how much room to we have for extra load?
      $room_for_load = $maxLoad - $currentLoad;
      print "room for load: $room_for_load\n";

      	 ###if we have more room than needed, we reserve space 
      	 ###just enough for that load.
      if ($room_for_load > $numload) {
          $addload = $numload;
      } 
      	 ### otherwise we just add as much as the room permits
      else {
          $addload = $room_for_load;
      }
      print "addload: $addload\n";

      	 ###if we have room for load, we load.
	 ## this will fail. stdquery has AND stmt. 
	 ## cant use with UPDATE stmt. RKS.
      	    ## my $stdquery =" AND StarDes ='".$system_des."' AND OrbitDes ="
	      ## .$orbit_des." AND TurnTillActive=".$distance
	      ## ." where GameNo=".$GN." AND ShipNo=".$shipno
	      ## . " AND Faction='".$name."' AND ShipType='Transport'";

      $stdquery =", StarDes ='".$system_des."', DesSysNo = " .
	  findIndex('Planet', $system_des) . ", OrbitDes ="
	  . $orbit_des . ", TurnTillActive=".$distance
	  . " WHERE GameNo= " . $GN . " AND ShipNo=".$shipno
	  . " AND OwnerFactionName='".$name."' AND ShipType='Transport'";

      if ( $addload > 0 ) {
       if ($load_type eq 'Raw Materials') {
           $totalrmload = $addload + $rmload;

           $q14 = "UPDATE Ship SET RawMat = " . $totalrmload . $stdquery;
           operate_on_DB($q14);

           $Planet->[$systemNo][$orbit]->change_rm(-$addload);
		## Hmmm. I think Factories should be Factory
		## changed to Factory. RKS
        } 
	elsif ($load_type eq 'Factory') {
           $totalfacload = $addload + $facload;
           $q14 = "UPDATE Ship SET Fac = " . $totalfacload . $stdquery;
           operate_on_DB($q14);
           $Planet->[$systemNo][$orbit]->change_fac(-$addload);
        } 
	elsif ( $load_type eq 'Shock Troops' ) {
           $totalstload = $addload + $stload;
           $q14 = "UPDATE Ship SET Troops = " . $totalstload . $stdquery;
           operate_on_DB($q14);
           $Planet->[$systemNo][$orbit]->change_st(-$addload); 
	}
	else {
	   print "I dont recognize that load type: $load_type\n";
        }

        $numload -= $addload;

      } ## end if ( $addload > 0 ) 
      } ## end if ( $currentLoad < $maxLoad ) 
  } ## end while loop
  $sth13->finish;
} ## end function

## enough verifies that there are enough ships for the transport order to
## succeed. returns 1 if enough transports. 0 otherwise(failing order)
sub enough {
   my ( $systemNo, $orbitNo, $playerName, $load, $num) = (@_);
   my $doTransport = 0;
   my $availableResource = 0;
   my $availableSlots = 0;
   my $usedSlots = 0;
   my $maxSlots = 5;

   print "enough. system: $systemNo, orbit: $orbitNo, ";
   print "name: $playerName, loadtype: $load numLoad: $num\n";

  	## verify load type and number of them are on planet
   if ( $load eq 'Factory' ) {
      if ( $num <= $Planet->[$systemNo][$orbitNo]->numFac() ) {
         $availableResource = 1;
      }
   }
   elsif ( $load eq 'Mine' ) {
      if ( $num <= $Planet->[$systemNo][$orbitNo]->numMines() ) {
         $availableResource = 1;
      }
   }
   elsif ( $load eq 'Shock Troops' ) {
      if ( $num <= $Planet->[$systemNo][$orbitNo]->Troops() ) {
         $availableResource = 1;
      }
   }
   else {
	print "I dont know that type. Cant transport: $load\n";
   }
   
        ## find all transports for given star and orbit
   $qq = "SELECT * from Ship WHERE SysNo = " . $systemNo .
        " AND Orbit = " . $orbitNo . " AND OwnerFactionName = '" .
        $playerName . "' AND ShipType = 'Transport' AND GameNo = " .
	$GN;
   $sthqq = $dbh->prepare($qq);
   $sthqq->execute;

        ## find available slots for transports
   while ( $tranport_ref = $sthqq->fetchrow_hashref ) {
      $usedSlots = $tranport_ref->{'RawMat'} +
         $tranport_ref->{'Fac'} + $tranport_ref->{'Troops'};

      $availableSlots += ( $maxSlots - $usedSlots );
   };
   $sthqq->finish;

        ## if available slots return 1.
   if ( $availableSlots >= $num ) {
      $doTransport = 1;
   }
   print "availslots: $availableSlots return (doTransport): $doTransport\n";
   print " && available Resource: $availableResource\n";
   print "VERIFY THIS FUNCTION QUERIES FROM THE DB.\n";

   if ( $availableResource == 1 && $doTransport == 1) {
      return 1;
   }
   else {
      return 0;
   }
}

### for all ships with TurnTillActive > 0, decrease value by one.
sub updateShip {
   my ($gameNo) = (@_);

   print "updating Ship TurnTillActive. \n";
   $qq2 = "SELECT * from Ship WHERE GameNo = " . $gameNo . 
	" AND TurnTillActive > 0";
   $sthqq2 = $dbh->prepare($qq2);
   $sthqq2->execute;
   $ship_ref = $sthqq2;
   ## $temp = $sthqq2->fetchrow_hashref;
   ## print "checking shipno: $temp->{'ShipNo'} for game: $gameNo\n";

   ## while ( $ship = $ship_ref->fetchrow_hashref ) {
   while ( $ship = $sthqq2->fetchrow_hashref ) {

      print "selected shipno: $ship->{'ShipNo'}\n";
      $newValue = $ship->{'TurnTillActive'} - 1;

      if ( $newValue > 0 ) {
      $qq3 = "UPDATE Ship SET TurnTillActive = " . 
	 $newValue . " WHERE GameNo = " .
	 $GN . " AND OwnerFactionName = '" . $ship->{'OwnerFactionName'} .
	 "' AND ShipNo = " . $ship->{'ShipNo'};
      $sthqq3 = $dbh->prepare($qq3);
      $sthqq3->execute;
      $sthqq3->finish;
      }
      	 ## ship has arrived at its destination. update Star, SysNo, Orbit info
      else {
      $qq4 = "UPDATE Ship SET TurnTillActive = " . 
	 $newValue . ", Star = '" . $ship->{'StarDes'} . "', SysNo = " .
	 $ship->{'DesSysNo'} . ", Orbit = " . $ship->{'OrbitDes'} .
	 " WHERE GameNo = " .
	 $GN . " AND OwnerFactionName = '" . $ship->{'OwnerFactionName'} .
	 "' AND ShipNo = " . $ship->{'ShipNo'};
      $sthqq4 = $dbh->prepare($qq4);
      $sthqq4->execute;
      $sthqq4->finish;
      }
      
      print "just updated ship no: $ship->{'ShipNo'} ";
      print "for $ship->{'OwnerFactionName'}\n";
   }
   $sthqq2->finish;
 
}

### move order fail if we're trying to move more ships than we have
sub move {
	 ## $system is System char
        my ( $order_ref, $system, $orbit) = @_;
        my $name = $order_ref->{'FactionName'};
        my $system_des = $order_ref->{'SystemDes'};
        my $orbit_des = $order_ref->{'OrbitDes'};
        my $shiptype = $order_ref->{'ObjectType'};
        my $num_ships = $order_ref->{'NumObject'};

	print "move:: system==$system, orbit==$orbit, name==$name\n";
	print "-->TO system_des==$system_des, orbit_des==$orbit_des\n";
	print "-->WHAT shiptype==$shiptype, num_ships==$num_ships\n";

	  ## sub calcturns(systemTEXT, systemNO)...dont ask me why. RKS
	  ## sera's doing. finxing params below. RKS
          ## my $distance = calcturns(findIndex('Planet',$system), 
	  ## 			findIndex('Planet', $system_des));

        my $distance = calcturns(findIndex('Planet', $system), 
				findIndex('Planet', $system_des));

        $q15 = "SELECT * FROM Ship where GameNo= " 
		. $GN . " AND OwnerFactionName='" . $name . 
		"'  AND ShipType='" . $shiptype . "' AND Star='" . 
		$system . "' AND Orbit=" . $orbit 
		. " AND TurnTillActive = 0 ORDER BY ShipNo";

        ### fail order unless we have enough ships to move

	my $test_q = $q15;
	my $test = returnDBrow($test_q);
	print "move:: ships found==$test >= $num_ships or return\n";
        return unless ($test >= $num_ships);

	$sth15 = $dbh->prepare($q15);
        $sth15->execute;

	   ## used for debugging. RKS
	   ## $test = $sth15->fetchrow_hashref;
	   ## $test1 = $test->{'ShipNo'};
	   ## print "testing $test1\n";

        while (( $ship_ref = $sth15->fetchrow_hashref) && $num_ships > 0) {

	print "num_ships: $num_ships ship no: $ship_ref->{'ShipNo'}\n";

             $q16 = "UPDATE Ship SET TurnTillActive = " . $distance 
		. ", StarDes ='".$system_des."', OrbitDes=" 
		. $orbit_des ." where GameNo= " . $GN . 
		" AND OwnerFactionName='" . $name . "' AND ShipNo = "
	 	. $ship_ref->{'ShipNo'} 
			## this loop should apply to any ship, not just
			## transports. fixed. RKS.
			## ."' AND ShipType='Transport' AND Star='".$system 
		. "  AND ShipType='" . $shiptype . "' AND Star='" . $system 
		. "' AND Orbit=" . $orbit . " AND TurnTillActive = 0";

	     ## operate_on_DB($q16);
             $sth16 = $dbh->prepare($q16);
             $sth16->execute;
             $sth16->finish; 

             $num_ships--;
	    
        }
        $sth15->finish;
}

sub calcturns {
    my ($system, $des) = @_;

    	## system is TEXT, des is systemNO. sera's work. RKS.
	## fixed. $system is now systemNo. RKS

    $test = int(distance($system, $des)/5) + 1;
    print "return $test...do the math\n";

return int(distance($system, $des)/5) + 1;
}

sub distance {
    my ($sysNo, $desNo) = @_;
    	## sys is systemTEXT, desNo is systemNO. sera's work. RKS.
	## fixed. $system is now systemNo. RKS
    my $sys = findString('Planet',$sysNo);
    my $des = findString('Planet',$desNo);

    print "star origin: $sys, star dest: $des\n";

    my $q= "SELECT * from System where Star='" . $sys 
		. "' AND GameNo = " . $GN;
    my $sth= $dbh->prepare($q);
    $sth->execute;

    my $system_ref = $sth->fetchrow_hashref;

    $sth->finish;

    my $x1 = $system_ref->{'X_Coor'};
    my $y1 = $system_ref->{'Y_Coor'};
    my $z1 = $system_ref->{'Z_Coor'};

    $q= "SELECT * from System where Star='" . $des. "' AND GameNo = " . $GN;
    $sth= $dbh->prepare($q);
    $sth->execute;

    my $des_ref = $sth->fetchrow_hashref;

    $sth->finish;

    my $x2 = $des_ref->{'X_Coor'};
    my $y2 = $des_ref->{'Y_Coor'};
    my $z2 = $des_ref->{'Z_Coor'};

print "GameNo: $GN x1: $x1 x2: $x2 y1: $y1 y2: $y2\n";

    return int(sqrt(($x2-$x1)*($x2-$x1) + ($y2-$y1)*($y2-$y1)));
}


## I'll leave the Ally table in string because with numbers 
## it won't make much sense. Sera's note.
## Doens't make sense anyway, 
## don't need system or orbit for function. RKS.
  
sub ally{
	  ## $system is SystemNo
	  ## changed. $system, $orbit not being used. RKS.
	  ## my ( $order_ref, $system, $orbit) = @_;

       my ( $order_ref ) = @_;
       my $name = $order_ref->{'FactionName'};
       my $ally_name = $order_ref->{'TargetName'};
          ### Prevent multiple similar ally declaration
       $q17 = "SELECT * FROM Allied where GameNo= " . $GN 
		. " AND ThisFactionIs='" . $name 
		. "'  AND AlliedToFaction='" . $ally_name . "'";
        return unless (returnDBrow($q17) ==0);
        $q18 = "INSERT INTO Allied VALUES (" . $GN . ",'" 
		. $name . "','" . $ally_name . "')";
        operate_on_DB($q18);
}

sub unally{
	## $system is SystemNo
	## changed. $system, $orbit not being used. RKS.
        ## my ( $order_ref, $system, $orbit) = @_;
       my ( $order_ref ) = @_;
       my $name = $order_ref->{'FactionName'};
       my $ally_name = $order_ref->{'TargetName'};
        ### Prevent multiple similar unally declaration
        ## verifies player is allied to target name
       $q19 = "SELECT * FROM Allied where GameNo= " . $GN 
		. " AND ThisFactionIs='" . $name 
		. "'  AND AlliedToFaction='" . $ally_name . "'";
        return unless (returnDBrow($q19) >0);
       $q20 = "DELETE FROM Allied where GameNo=" . $GN . 
		" AND ThisFactionIs='" . $name . 
		"' AND AlliedToFaction='" .$ally_name."'";
        operate_on_DB($q20);
}  

   # IN: ord(er)_ref, systemNO, orbit
sub security {
   my ($ord_ref, $s, $o) = (@_);   
   my $pNo = findIndex('PlayerStat', $order_ref->{'FactionName'});
   my $num = $order_ref->{'NumObject'};
   my $industry = $Player[$pNo]->industry();

   	## make sure code in Planet->cant_produce is correct
	## looks OK. RKS.

   if ( $Planet->[$s][$o]->ownerName() eq $ord_ref->{'FactionName'} ) {
      $Planet->[$s][$o]->increase_security($industry, 
			$Player[$pNo]->espionage(),$num,1);
   }
   else {
      print "$ord_ref->{'FactionName'} cant make ";
      print "security policies on System $s Orbit $o\n";
   }
return 1;
}

	### Build order always send a $buildfor. In case of building for
	### oneself the $buildfor is one's name.
	### We deal with $name as number in the beginning, and then after we figure out
	### the planets, but for ships, once we get to the subroutines that actually
	### creates the entry, name gets back to string because Ship uses strings.
        ## Tested build. looks good. need to verify build as noted below. RKS
sub build {
	## $sys is SystemNo 
	## $name is player number
   my ($order_ref, $sys, $orbit) = @_;
   my $name = findIndex('PlayerStat', $order_ref->{'FactionName'});
   my $buildtype = $order_ref->{'ObjectType'};
   my $num = $order_ref->{'NumObject'};
   my $industry = $Player[$name]->industry();
   my $buildfor = findIndex('PlayerStat', $order_ref->{'TargetName'});

   ## added to handle building for oneself. TargetName is only
   ## assigned if for someone else. RKS
   if ( !$buildfor) {
	$buildfor = $name;
   }

   print "$name from $sys $orbit with industry ";
   print "$industry build $num $buildtype \n";

   if ($Planet->[$sys][$orbit]->owner()!=$name) {
      print "Build failed. You do not own system $sys orbit $orbit.\nc";
      return 0;
   }

   	## tested. needs to be used on non-starting planet RKS
   if ($buildtype eq 'Mine') {
      return $Planet->[$sys][$orbit]->build_mines($industry, $num);
   } 
   	## tested. needs to be used on non-starting planet. RKS
   elsif ($buildtype eq 'Factory') {
      return $Planet->[$sys][$orbit]->build_factories($industry, $num);
   } 
   	## tested. RKS
   elsif ($buildtype eq 'Shock Troops'){
      return $Planet->[$sys][$orbit]->build_shock_troops($industry, $num);
   } 
   	## tested. RKS
   elsif ($buildtype eq 'Base') {
      return $Planet->[$sys][$orbit]->build_bases($industry, $num);
   } 
   	## tested. RKS
   elsif ($buildtype eq 'Frigate') {
      if ($Planet->[$sys][$orbit]->build_ships($industry, 25*$num)) {  
         addShip($sys, $orbit, 'Frigate', $name, $buildfor, $num, 1);} 
      return;
   } 
   	## tested. RKS
   elsif ($buildtype eq 'Transport') {
      if ($Planet->[$sys][$orbit]->build_ships($industry, 10*$num)) {  
         addShip($sys, $orbit,'Transport', $name, $buildfor, $num, 1);} 
      return;
   } 
   	## tested. RKS
   elsif ($buildtype eq 'Battleship') {
      if ($Planet->[$sys][$orbit]->build_ships($industry, 50*$num)) {  
         addShip($sys, $orbit,'Battleship',$name,$buildfor, $num, 1);} 
      return;
   } 
   else {
      print "I don't recognize buildtype $buildtype \n";
   } 
}

sub addShip {
        my ($sysno, $orbit, $shiptype, $no, 
	   	$contractor_no, $num, $update) = @_;
        print "Player $no of system $sysno orbit $orbit built ";
	print "$num $shiptype for Player $contractor_no\n"; 
        my $maint = $num; my $i=0;
        my $sysportno = 0;
        my $orbit_port = 0; 

        if ($shiptype eq 'Battleship') {
	   $maint = 2*$num;
	} 

        if (($no==$contractor_no) || !($contractor_no)) {
              $sysportno = $sysno;
              $orbit_port = $orbit;
              if ($update) {
	         $Planet->[$sysno][$orbit]->changeMaintananceBy($maint);
	      }
	} 
	else {
	   $no	 = $contractor_no;

		## get the Player's info
           my $q99 = "SELECT * FROM PlayerStat where GameNo= " . $GN .
		" AND PlayerNo = " . $no;
           my $sth99 = $dbh->prepare($q99);
           $sth99->execute;
	   $player_ref = $sth99->fetchrow_hashref;
           $sth99->finish;
	   
		## get sysno for contractorNo. added by RKS
		## will be homeportno from PlayerStat dB. RKS
	   $sysno = $player_ref->{'HomePortNo'};
	   
		## assign sysportno to sysno for contractorNo. added by RKS
	   $sysportno = $sysno;

		## get orbit_port for contractorNo. added by RKS
	   $orbit_port = $player_ref->{'HomePortOrbit'};

		## do update maintanance for contractor planet . added by RKS
           if ($update) {
	      $Planet->[$sysno][$orbit]->changeMaintananceBy($maint);
	   }
        }

	   ## code was making a contracted ship's homeport the builders
	   ## this has problems with maintenance and changing ownership
	   ## best to use the contracted plyaers starting homeport. RKS

        my $name = findString ('PlayerStat', $no);

        my $system = findString ('Planet', $sysno);
        my $system_port = findString ('Planet', $sysportno);

	my $nextShipNo = getLastShipNo( $GN, $name) + 1;

        for ($i=0; $i < $num; $i++) {
		## removing from code. using $nextShipNo. RKS
	   ## $SN++;
           ## $q21 = "INSERT INTO Ship VALUES (".$GN.",".$no.",'".
		## $name."','".$name."','".$shiptype."',".$SN.",'".
		## $system."',".$sysno.",".$orbit.",0,'',0,0,'".
		## $system_port."',".$sysportno.",".$orbit_port.",0,0,0,0)" ;     
           $q21 = "INSERT INTO Ship VALUES (" . $GN . "," . $no . ",'" .
		$name . "','" . $name . "','" . $shiptype . 
		"'," . $nextShipNo . ",'" . $system . "'," . 
		$sysno . "," . $orbit . ",0,'',0,0,'" . 
		$system_port . "'," . $sysportno . "," . 
		$orbit_port . ",0,0,0,0)" ;     
           operate_on_DB($q21);
		## increment $nextShipNo for next Ship Number
	   $nextShipNo++;
	}
}

## need select from ship ordering by shipno in decending order
## get first (highest) no, increase by 1, use for ship no.
sub getLastShipNo {
   my ( $GN, $name) = @_;
   my $shipNo = -1;

 	## order the players ships be shipno in descending order
   $qq1 = "SELECT * FROM Ship WHERE GameNo = " . $GN . 
	" AND OwnerFactionName = '" . $name . "' ORDER BY ShipNo DESC";
   $sthh1 = $dbh->prepare($qq1);
   $sthh1->execute;

	## get the first, and largest number, from the values returned
   $Ship_ref = $sthh1->fetchrow_hashref;

	## assign to var. and return
   $shipNo = $Ship_ref->{'ShipNo'};
   $sthh1->finish;
print "shipNo: $shipNo\n";

return $shipNo;
}

sub getResourceCountOnShip {
   my ($load_ref, $entityName) = (@_);
   if ( $entityName eq 'RawMat' ) {
      return $load_ref->{'RawMat'};
   }
   elsif ($entityName eq 'Fac' ) {
      return $load_ref->{'Fac'};
   }
   elsif ($entityName eq 'Troops' ) {
      return $load_ref->{'Troops'};
   }
   else {
      print "I dont know that db reference: $entityName\n";
   }
}

sub unload {
 ## $system is SystemNo
       my ( $order_ref, $system, $orbit) = @_;
       my $name = $order_ref->{'FactionName'};
       my $load_type = $order_ref->{'ObjectType'};
       my $num = $order_ref->{'NumObject'};
       my $loadDB = '';

       print "unloading. for $name $num $load_type on system $system $orbit\n";

	 ## unloads to the planet first. then checks to see if everything
	 ## is OK. sera's fine work. RKS.
       if ($load_type eq 'Factory') {
		## adding loadDB to minimize code in next function call. RKS
	 $loadDB = 'Fac';
    	 return 0 unless ($Planet->[$system][$orbit]->change_fac($num));
       }
       elsif ($load_type eq 'Shock Troops') {
		## adding loadDB to minimize code in next function call. RKS
	 $loadDB = 'Troops';
	 return 0 unless ($Planet->[$system][$orbit]->change_st($num));
       }        
       elsif ($load_type eq 'Raw Materials') {
		## adding loadDB to minimize code in next function call. RKS
	 $loadDB = 'RawMat';
	 return 0 unless ($Planet->[$system][$orbit]->change_rm($num));
       }        
       else {
        print "I dont recognize that load type: $load_type\n";
	return 0;
       }
	 ## sera's doing. RKS.
         ## if ($load_type eq 'Factory') {
     	 ## return 0 unless $Planet->[$system][$orbit]->change_fac($num);
         ## }
         ## if ($load_type eq 'Shock Troops') {
	 ## return 0 unless ($Planet->[$system][$orbit]->change_st($num) || 
	 ## $Planet->[$system][$orbit]->owner() != $name);
         ## }        

       print "going to unload by load type: $load_type, ";
       print "using $loadDB as entity to write to the dB\n";

       unload_according_to_load_type($load_type, $loadDB, 
	 	$num, $system, $orbit, $name);
}

##// having problems with dBentity
	## system is systemNo
sub unload_according_to_load_type {
   my ($load_type, $dBentity, $num, $system, $orbit, $name)=@_;
   my $total = 0;
   my $shipno=0;

   print "unload_according_to_load_type\n";
   my $query = " WHERE OwnerFactionName='" . $name
	. "' AND ShipType='Transport' AND Star = '" 
	. findString('Planet', $system) . "' AND Orbit=" 
	. $orbit . " AND TurnTillActive=0 AND " 
	. $dBentity ." > 0";

	## Sera's interesting attempt at minimizing code
	## but Im afraid its not going to happen in this version. RKS
	## turns out with a litle help from above I can make this work.
	## notice addtion of $load in above function. RKS
	## . $load_type ." > 0";

   $q22 = "SELECT * FROM Ship" . $query;
   $sth22 = $dbh->prepare($q22);
   $sth22->execute;

   	### If we have no more load of that type, we stop. 
   	### we unload what we can. Order is always successful
   	### even if we try to unload more than we have.
   	## edited code below || to &&. RKS
        ## while ( $load_ref = $sth22->fetchrow_hashref || $total < $num ){
   while ( $load_ref = $sth22->fetchrow_hashref && $total < $num ){

     $shipno = $load_ref->{'ShipNo'};

     ## sera attempt. RKS
     ## $total += $load_ref->{'$dBentity'}; 
     $total += getResourceCountOnShip($load_ref, $dBentity);

     $q23 = "UPDATE Ship SET " . $dBentity . " = 0 " . $query .
	" AND ShipNo = " . $shipno;
     operate_on_DB($q23);                 
   }
   $sth22->finish;

   my $difference = $total-$num;
   	### we unloaded too much stuff, 
	### stick it back in the last ship we unloaded.
	## seems difference != 0 ever.RKS
   	## if ($difference > 0) {
   if ($difference != 0) {
       $total = $num;
       $q24 = "UPDATE Ship SET ".$load_type."="
		.$difference.$query." AND ShipNo=".$shipno;
       operate_on_DB($q24);                 
   } 
   elsif ($difference < 0 ){
       	   ### We unload less than the intended amount.
       	   ### need to take out the ones we presumptuosly added
      if ($load_type eq 'Raw_Materials') { 
         $Planet->[$system][$orbit]->change_rm($difference);
      } elsif ($load_type eq 'Factory') { 
         $Planet->[$system][$orbit]->change_fac($difference);
      } elsif (($load_type eq 'Shock Troops') && 
		($Planet->[$system][$orbit]->owner() eq $name)) { 	
         	   ##adding shock troops to one's own $Planet
         $Planet->[$system][$orbit]->change_st($difference);
      } 
      else {
          ## it's an attack!! Can only be done when thereís no bases
          ## because the bases are mightly killing machines!
          ## if there's a base the shock troops had been wasted.
	 if (!($Planet->[$system][$orbit]->bases()))	{	
            $Planet->[$system][$orbit]->attacker_take_over_Planet(
		$name, $Player[$name]->race(), 
		$total, $Player[$name]->infantry());
	 }
  
      }								
   }
}

### if a spy attempt succeed, this sub returns a list of info.
sub spy {
	   ## $system is SystemNo
print "Beginning of sub spy\n";
       my ($order_ref, $system, $orbit) = @_;
       my $name = $order_ref->{'FactionName'};
       my $pno = findIndex('PlayerStat', $name);
       my $num_prod = $order_ref->{'NumObject'};
       my $system_des = $order_ref->{'SystemDes'};
       my $orbit_des = $order_ref->{'OrbitDes'};
	   ## debugging. can_produce doesnt exist. RKS
	   ##  return 0 unless 
	   ##  	$Planet->[$system][$orbit]->can_produce( $num_prod, 
	   ##		$Player[$name]->Industry() );
	   ##  error in Player object
	   ##  fixed below...
	   # 	print "In main::spy::system==$system\n";
	   # 	print "In main::spy::orbit==$orbit\n";
	   # 	print "In main::spy::player==$name\n";
	   # 	print "Going to cant_produce\n";
print "Middle of sub spy\n";
	if ($Planet->[$system][$orbit]->cant_produce( 
		$Player[$pno]->industry(), $num_prod ) != 0) {
	   return 0;
	}

       	## return 0 unless $Planet->[$system][$orbit]->cant_produce(
	## $Player[$pno]->industry(),
	## $num_prod );

       my $system_des_NO = findIndex('Planet', $system_des);
       my $system_STRING = findString('Planet', $system);

    	 ## error by sera. 
      	 ## my $distance =distance($system_des, $system);
       my $distance = int(distance($system_STRING, $system_des));
       my $attempt_value = 
	($Player[$pno]->espionage() - $distance)*$num_prod;
       return unless 
	   ($Planet->[$system_des_NO][$orbit_des]->espionage(
		$attempt_value));
       $q25 = "INSERT INTO SpyResult VALUES (" . $GN . ",'" . $name 
		. "','" . $system_des . "'," . $orbit_des . ")";
      operate_on_DB($q25); 
print "Destination system: $system_des systemNo: $system_des_NO: ";
print "orbit: $orbit_des.\nEnd of sub spy\n";
}

#### Attack can be very specific, e.g : Attack Faction A w/ 4 bases
#### All this function do is figure out the attack value of this order, 
#### enter it into the overrun table to be totalled up and computed.
sub attack { 
	    ## $system is System char
      my ( $system, $orbit) = @_;
      my $b_ship = 0; 
      my $frigate = 0; 
      my $base = 0; 
      my $object = '';
      my $numobject = 0;
      my $attacker = '';
      my $defender = '';
      my $attval = 0;
      my $defval = 0;
      my $overrun_defense = 0;
      my $damage_done = 0;
      my $overrun = 0;
      my $magicNumberEleven = 11;
      my $Fname = '';
      my $Fno = -1;
      my $overrun_ratio = -1;
      my $overrun_test = -1;

print "In attack:: system: $system orbit: $orbit\n";

      my $standard_query =  " FROM Orders where GameNo = " . $GN
	   . " AND OrderType = 'attack' AND System = '" 
	   . $system . "' AND Orbit = " . $orbit;

	   ## this will query all faction with orders 
	   ## at the planet who are attacking. But, DISTINCT does
	   ## not work with fetchrow_hashref. modified by RKS.
      	   ## $q26 = "SELECT DISTINCT FactionName " . $standard_query;

      $q26 = "SELECT *" . $standard_query;
      $sth26 = $dbh->prepare($q26);
      $sth26->execute;

	   ## modified by RKS 
           ## while ( my $attacker = $sth26->fetchrow_hashref($q26)) {

      while ( $attacker = $sth26->fetchrow_hashref) {

print "--> attacker( is hashref...): $attacker->{'FactionName'}\n";

	   ## DISTNINCT does not work with hashref. fixed. RKS
           ## $q27 = "SELECT DISTINCT TargetName " . $standard_query 

         $q27 = "SELECT *" . $standard_query 
		. " AND FactionName = '". $attacker->{'FactionName'} ."'";
         $sth27 = $dbh->prepare($q27);
         $sth27->execute;

	      ## this while loop handles multiple attacks by a single
	      ## attacker. RKS

	      ## modified by RKS 
              ## while (my $defender = $sth27->fetchrow_hashref($q27)) {

         while ( $defender = $sth27->fetchrow_hashref) {

	      ## must admit. Im stymied. Why is Sera using FactionName for
	      ## both attacker and defender? RKS
	      ## changing to TargetName. RKS

## print "defender( is hashref...): $defender->{'FactionName'}\n";
print "--> defender( is hashref...): $defender->{'TargetName'}\n";

             $q28 = "SELECT * " . $standard_query 
		. " AND FactionName = '". $attacker->{'FactionName'} 
		    ## . "' AND TargetName = '" .$defender->{'FactionName'} . "'";
		. "' AND TargetName = '" .$defender->{'TargetName'} . "'";
             $sth28=$dbh->prepare($q28);
             $sth28->execute;

		  ## now we have all orders with attacker and defender. RKS

	          ## modified by RKS 
                  ## while ($order_ref = $sth28->fetchrow_hashref($q28)) 

             while ( $order_ref = $sth28->fetchrow_hashref) {
                  $object = $order_ref->{'ObjectType'};
                  $numobject = $order_ref->{'NumObject'};
                  if ($object eq 'Battleship') {
			$b_ship += $numobject;
                  }
	 	  elsif ($object eq 'Frigate') {
			$frigate += $numobject;
                  }
		  elsif ($object eq 'Base') {
			$base += $numobject;
                  }
		  else { 
			print "$attacker->{'FactionName'} attack error: ObjectType.\n";
		  }  	## end if
             } 		## end while $q28

             $sth28->finish;

		## // checking out total_combat_level. RKS
             $attval = total_combat_level (
			'Attack', $system, $orbit, 
			     ## why is '0' being passed. Not in function. RKS
			     ## indicates 'attack'. RKS
			     ## changing order of params. '0' at end. RKS
			     ## $attacker->{'FactionName'},$b_ship,$frigate,0, $base);
			$attacker->{'FactionName'}, $b_ship, $frigate, $base, 0);

print "--> attval from total_combat_level: $attval\n";

		## cant be right, defense value return with -1 as last param.
		## poorly written code. needs coder to be examined with 
		## an anal probe.
		## modified. RKS
             		## $defval = total_combat_level (
				## 'Defense', $system, $orbit, 
				## $defender->{'FactionName'}, -1, -1, -1, -1);
             	$defval = total_combat_level (
			'Attack', $system, $orbit, 
			$defender->{'TargetName'}, 0, 0, 0, -1);

print "--> defval from total_combat_level: $defval\n";

             $overrun_defense = $defval + allies_total_defense_level(
		   	$system, $orbit, $defender->{'TargetName'});

		## FActionName should have been TargetName. fixed. RKS
		   	## $system, $orbit, $defender->{'FactionName'});

print "--> overrun_defense: $overrun_defense \n";

##
## whatis this doing??? left by sera. $attack and $name are not initialized
## fixed. RKS

	     $Fname = $attacker->{'FactionName'};
	     $Fno = findIndex('PlayerStat', $Fname);

		## name does not exist. fixed. RKS
	     	## $overrun_ratio = $magicNumberEleven - $Player[$name]->tactics();

	     $overrun_ratio = $magicNumberEleven - $Player[$Fno]->tactics();

		## save til I talk to Geoff. RKS
	     	## $overrun_test = $total_attack - $total_defense;

	     $overrun_test = int( $attval / $overrun_defense );

	     if ( $overrun_test > $overrun_ratio ) {

		## successful overrun
		## write the dB. RKS
		## what is $overrun. left by sera. RKS
		## when $overrun is '1', it means success. RKS
		## fixed. RKS
		## what is $damage_done. left by sera. RKS.
		## dont know. using $attval for now. FIXME. RKS
		##	$defender->{'TargetName'} . "'," . $overrun . 
		## 	$damage_done . ")";

		$damage_done = $attval;

                $q29 = "INSERT INTO Overrun VALUES (" . $GN . 
			",'" . $attacker->{'FactionName'} . "','" .
			$defender->{'TargetName'} . "', 1, " . 
			$damage_done . ")";

                operate_on_DB($q29);
  	     }

		## above code handling this mahem. RKS
             	## $overrun = 
			## ($attack > ($magicNumberEleven - 
				## $Player[$name]->tactics()) * $overrun_defense);

			   ## FActionName should be TargetName. fixed. RKS
			   ## $defender->{'FactionName'}. "',".$overrun . 

         } 		## end while $q27

         $sth27->finish;
       } 		## end while $q26

       $sth26->finish;
}

sub process_overrun_table {
       my ( $system, $orbit) = @_;

print "process_overrun_table:: system: $system orbit: $orbit\n";
print "--> functions commented out. RKS\n";

       ## total_up_attack_value($system, $orbit);
       ## enter_overruns($system, $orbit);
       ## compute_overrun_result($system, $orbit);
       ## computer_normal_combat($system, $orbit);

}

##### All the QUERIES are done on OVERRUN table
sub compute_overrun_result {
        my @loser = (); 
	my $i=0;
	my $stdquery = "";

        ## now we have the list of individual attack results, 
	## we figure out who did not get to attack because 
	## he was first overruned
        $q30 = "SELECT * from Overrun where GameNo=" . 
	   $GN ." AND Has_Overrun = 1";
        $sth30= $dbh->prepare($q30);
        $sth30->execute;
        while ($overrun_ref = $sth30->fetchrow_hashref) {
		## added findIndex to $name,$target to get PlayerNo
          $name = findIndex(
	    'PlayerStat', $overrun_ref->{'AttFactionName'} );
          $target = findIndex(
	    'PlayerStat', $overrun_ref->{'DefFactionName'} );
          ## check if both $target and $name are both eligible for overrun
          $q31 = $q30 . " AND AttFactionName = '" .
	    $target. "' AND DefFactionName = '" .$name."'";
          if (returnDBrow($q31)==0) {
             $loser[$i]=$target;
          } else { 
            if ($Player[$target]->tactics() > $Player[$name]->tactics())
               {$loser[$i]=$name;} 
            elsif($Player[$target]->tactics() < $Player[$name]->tactics())
               {$loser[$i]=$target;}
            elsif($Player[$target]->attack() > $Player[$name]->attack())
               {$loser[$i]=$name;} 
            elsif($Player[$target]->attack() < $Player[$name]->attack())
               {$loser[$i]=$target;}
            elsif($Player[$target]->sensor() > $Player[$name]->sensor())
               {$loser[$i]=$name;} 
            elsif($Player[$target]->sensor() < $Player[$name]->sensor())
               {$loser[$i]=$target;
            } else {
               ## nobody overruns, calculate like normal combat
               ## sera. RKS fixed query.
	       ## my $stdquery = "UPDATE HasOverrun=0 FROM Overrun WHERE GameNo=" .$GN. " AND HasOverrun = 1 AND AttFactionName ='";
               $stdquery = 
		 "UPDATE Overrun SET Has_Overrun=0 WHERE GameNo=" .
		 $GN. " AND Has_Overrun = 1 AND AttFactionName ='";
               $q32 = $stdquery.$name."' AND DefFactionName='"
		 .$target."'";
               $q33 = $stdquery.$target."' AND DefFactionName='".
		  $name."'";
               operate_on_DB($q32);
               operate_on_DB($q33);
            }
          }
     }
     $sth30->finish;
     foreach $loser (@loser) {
       $q34 = "DELETE FROM Overrun where GameNo=".$GN.
	 " AND AttFactionName='".$loser."'";
       $q35 = "DELETE FROM Overrun where GameNo=".$GN.
	 " AND DefFactionName='".$loser. "'";
       $q36 = "DELETE FROM Ship where GameNo=".$GN.
	 " AND Faction ='".$loser."' AND Star='".$system.
	 "' AND Orbit= ".$orbit." AND TurnTillActive = 0";
       operate_on_DB($q34);
       operate_on_DB($q35);
       operate_on_DB($q36);
       if ($Planet->[$system][$orbit]->owner() == $loser) {
             $Planet->[$system][$orbit]->lose_air_combat();
       }
    }
    $q37 = "DELETE FROM Overrun where GameNo=".$GN." AND Has_Overrun=1";
    operate_on_DB($q37);
}

sub computer_normal_combat {
       ### All overrun is done. Phew. There shouldn't be anymore record w/ Overrun=1
       ### Now go through the @damage done list        
       $q38 = "SELECT * from Overrun where GameNo=" . $GN ." AND Has_Overrun = 0";
       $sth38= $dbh->prepare($q38);
       $sth38->execute;
       while ($overrun_ref = $sth38->fetchrow_hashref) {
          $name = $overrun_ref->{'AttFactionName'};
          $target = $overrun_ref->{'DefFactionName'};
          $damage = $overrun_ref->{'DamageDone'};
          distribute_damage($damage, $target, $system, $orbit);
        }
       $sth38->finish;
       $q39 = "DELETE FROM Overrun where GameNo=" . $GN;
       operate_on_DB($q39);
}

sub distribute_damage {
    my ( $damage, $name, $system, $orbit) = @_;
	## added findIndex and change $Player[$name] to $Player[$tno] below
    my $tno = findIndex( 'PlayerStat', $name );
    my $shipno = 0;
    my $stdquery = " FROM Ship where GameNo=" .$GN. 
	" AND Faction='".$name."' AND System='".
	$system."' AND Orbit = ".$orbit.
	" AND TurnTillActive =0 AND ShipType='";   
    my $defense = $Player[$tno]->defense(); 
## should be ->Bases()
    while ($damage > 0 || $Planet->[$system][$orbit]->bases() > 0) {
      if (returnDBrow("SELECT *".$stdquery. "Battleship'")>0) {
        $damage-=deletedShips($stdquery,"Battleship'",2,$defense); 
      }elsif (returnDBrow("SELECT *".$stdquery. "Frigate'")>0) {
        $damage-= deletedShips($stdquery, "Frigate'",1,$defense);
      }elsif (returnDBrow("SELECT *".$stdquery. "Transport'")>0) {
        $damage-= deletedShips($stdquery, "Transport'",1,$defense);
      } else {
        $Planet->[$system][$orbit]->remove_bases(1);
        $damage-=$defense;
      }
    }
}

sub deleteShips  {
    my ($query, $shiptype, $maint, $defense) = @_;
    my $shipno = 0; 
    my $totaldefense = 0;
    if (returnDBrow("SELECT * ".$query.$shiptype)>0) {
      my $q="SELECT DISTINCT ShipNo " .$query.$shiptype;
      my $sth=$dbh->prepare($q);
      $sth->execute;
      while ($shipno= $sth->fetchrow_hashref) {
	operate_on_DB("DELETE ".$query.$shiptype.
	   " AND ShipNo=".$shipno); 
	$totaldefense += $defense;
	$Planet->[$system][$orbit]->deal_with_dead_ships($maint);
      }
      $sth->finish;
    }
    return $totaldefense;
}

## values passed to function from attack. RKS.
## what is '0' doing??? RKS
## $attval = total_combat_level (
## 'Attack', $system, $orbit, 
## $attacker->{'FactionName'}, $b_ship, $frigate, 0, $base);
## adding $att_def_flag to param list. RKS

sub total_combat_level {
      my ( $combat_type, $system, $orbit, $name, 
	$used_bship, $used_fship, $used_bases, $att_def_flag) = @_;

print "total_combat_level:: name: $name combat: $combat_type\n";
print "--> system: $system orbit: $orbit att_def_flag: $att_def_flag\n";
print "--> Battleship: $used_bship Frigate: $used_fship Bases: $used_bases\n";

		## DEBUG ME. RKS. working on it. RKS
		## // not finding Player object. I dont have a clue why.
		## // IDEA. $name is the player NO, not name
		## opposite is correct. system is CHAR, not systemNo. fixed. RKS

		## added playerNo. no need to call findIndex twice. RKS
      my $playerNo = findIndex('PlayerStat', $name);

      		## my $attack = $Player[findIndex('PlayerStat', $name)]->attack();
      		## my $defense = $Player[findIndex('PlayerStat', $name)]->defense();

      my $attack  = $Player[$playerNo]->attack();
      my $defense = $Player[$playerNo]->defense();

      my $sysNo = findIndex('Planet', $system);
print "--> system: $system sysNo == $sysNo\n";

      my $battleship = num_active($name, 'Battleship', 
	 	$used_bship, $system, $orbit);

      my $frigates = num_active($name, 'Frigates', 
		 $used_fship, $system, $orbit);

      my $transport = num_active($name, 'Transport', 
		 -1, $system,$orbit);

      if ($combat_type eq 'Attack') {
		 ## not sure what this is doing? 
		 ## functions not written by sera.
		 ## guess: unengagedBases::Planet->Bases - engaged bases. RKS.
       		 ## my $base = $Planet->[$system][$orbit]->engagedBases();

	 	 ## get engaged bases
		 ## passing '0', no change to 'Engaged Bases' var
		 ## changing system to sysNo. RKS
	 	 ## my $engagedBases = $Planet->[$system][$orbit]->engaged(0);
	 my $engagedBases = $Planet->[$sysNo][$orbit]->engaged(0);

		 ## get available bases
		 ## changing system to sysNo. RKS
       	 	 ## my $availBase=$Planet->[$system][$orbit]->Bases() - $engagedBases;
       	 my $availBase = $Planet->[$sysNo][$orbit]->Bases() - $engagedBases;
	 if ( $availBase < 0 ) {
	    print "attacking with bases when no bases available, \n";
	    print "available bases: $availBase setting to '0'\n";
	    $availBase = 0;
  	 }

		## unneeded query. RKS
	 	## my $q = "SELECT * from Planet WHERE Star='" . $system .
			## "' AND Orbit = " . $orbit . " and GameNo=" . $GN;
	 	## my $sth = $dbh->prepare($q);
	 	## $sth->execute;
	 	## my $base_ref = $sth->fetchrow_hashref;
	 	## my $base = $base_ref->{'NoBases'};
	 	## $sth->finish;

		## base is availBase
	 $base = $availBase;

		## its an attack
	 if ( $att_def_flag > -1 ) {
		## can use less than or equal to the number of bases
		## available. not just less than. fixed. RKS
         	## if ($used_bases < $base) {
             if ($used_bases <= $base) {
	         $base = $used_bases;
	 	    ## why is this here? what is it doing? No ideas. RKS.
	 	    ## guess what...$Planet object is not passed to this function
		    ## because system is CHAR, not INT
    
		    ## changing system to sysNo. RKS
             	    ## my $newEngagedBasesValue=
			## $Planet->[$system][$orbit]->engaged($base);
                 my $newEngagedBasesValue = $Planet->[$sysNo][$orbit]->engaged($base);
	     }
         return ($battleship * 3 + $frigates + $base) * $attack;
         } 
		## for defense, all bases are counted. RKS
	 else {
		## should be Bases(). fixed. RKS
             	## $base = $Planet->[$system][$orbit]->bases();  
		## changing system to sysNo. RKS
             	## $base = $Planet->[$system][$orbit]->Bases();  
             $base = $Planet->[$sysNo][$orbit]->Bases();  
             return ($battleship * 2 + $frigates + $transport + $base) * $defense;
      }
}

	## function call 
	## my $frigates = num_active($name, 'Frigates', 
	## $used_fship, $system, $orbit);
	
	## Best I can tell from Sera's code...
	## $ctype is:
	##	1) the number of ships attacking
	## 	2) 0, zero ships attacking. exit function
	##	3) -1, a defense calculation.

	## this function is setting shiptypes as Engaged. RKS
sub num_active {
    my ( $name, $ctype, $defendFlag, $system, $orbit) = @_;
    my $engaged = "";

print "num_active:: name: $name ctype(shiptype): $ctype defendFlag: $defendFlag\n";
print "--> system: $system orbit: $orbit\n";

    if ($defendFlag == 0) {
	return 0;
    }
		## cleaning house. RKS
    		## if ($defendFlag == -1) {
        	## ### a defense calculation. doesn't matter what's engaged.
        	## $engaged = "";
    		## } 
    		## else {
        	## $engaged = " AND Engaged = 0";
    		## }

    if ($defendFlag != -1) {
       $engaged = " AND Engaged = 0";
    }

		## again, cant use DISTINCT with fetchrow_hashref. RKS
    		## $q30 = "SELECT DISTINCT ShipNo FROM Ship where GameNo=" .

    $q30 = "SELECT * FROM Ship where GameNo=" .
	 $GN . " AND OwnerFactionName = '" . $name .  
	 "' AND ShipType = '" . $ctype . "' AND Star = '" . 
	 $system . "' AND Orbit = " . $orbit . 
	 " AND TurnTillActive = 0" . $engaged . " ORDER BY ShipNo"; 

		## dont know what this is doing. RKS
		## I dont think the query is necessary. but leave for now.
		## its not hurting anything...except performance. RKS

    if ($defendFlag == -1) {
	my $temp_rows_query = $q30;
	return returnDBrow($temp_rows_query);
    }

    $sth30 = $dbh->prepare($q30);
    $sth30->execute;

    while ( ( $ship_ref = $sth30->fetchrow_hashref) && $defendFlag > 0) { 
        $q31 = "UPDATE Ship SET Engaged = 1 where GameNo = " . 
	  $GN . " AND OwnerFactionName = '" . $name .  
		## only doing Battleship, should be specific. RKS
	  	## "' AND ShipType = 'Battleship' AND Star = '" . 
	  "' AND ShipType = '" . $ctype . "' AND Star = '" . 
	  $system . "' AND Orbit = " . $orbit . " AND ShipNo = " .
	  $ship_ref->{'ShipNo'}; 
        operate_on_DB($q31);

        $defendFlag--;

     }

     $sth30->finish;             
}

## function call from attack.
## $overrun_defense = $defval + allies_total_defense_level(
## $system, $orbit, $defender->{'TargetName'});
## system is CHAR
 
sub allies_total_defense_level {
       my ( $system, $orbit, $name) = @_;
       my $total = 0;

print "allies_total_defense_level:: system: $system orbit: $orbit name: $name\n";
		## and again, DISTOINCT will not work with hashref. RKS
	 	## "SELECT DISTINCT ThisFactionIs FROM Allied where GameNo= " . 

       $q32 = "SELECT * FROM Allied where GameNo= " . 
	    $GN . " AND AlliedToFaction='" . $name . "'";  
       $sth32 = $dbh->prepare($q32);
       $sth32->execute;
		## what is fetchrow_arrow. modified. RKS
       		## while ( my $ally = $sth32->fetchrow_arrow) {

       while ( $ally_ref = $sth32->fetchrow_arrow) {
my $test_ref = $ally_ref;
my $test = $test_ref->{'ThisFactionIs'};
print "--> ally == $test";

		## modified per changes to total_combat_level. RKS
          	## $total += total_combat_level('Defense', $system, 
			## $orbit, $ally_ref->{'ThisFactionIs'}, 0, 0, 0);
          $total += total_combat_level('Attack', $system, 
		$orbit, $ally_ref->{'ThisFactionIs'}, 0, 0, 0, -1);
print " total defense is increasing: $total\n";
       }
       $sth32->finish;
return $total;
}

## needs to be DEBUGGED. left unfinished by sera.
## all order costs happen
sub maintanance {
   ###go through each Planet
  $q50 = "SELECT * FROM Planet where GameNo= " . $GN;
  $sth50 = $dbh->prepare($q50);
  $sth50->execute;

  while ( $planet_ref = $sth50->fetchrow_hashref ){
      my $system= $planet_ref->{'SysNo'};
      my $orbit = $planet_ref->{'Orbit'};
      my $name = $planet_ref->{'OwnerFactionName'};
      my $q60 = "SELECT * FROM PlayerStat WHERE GameNo=" . $GN .
	   " AND FactionName='" . $name . "'";
      $sth60 = $dbh->prepare($q60);
      $sth60->execute;
      my $pl_ref = $sth60->fetchrow_hashref;
      $sth60->finish;
      
print "In main::maintanance::system==$system\n";
print "In main::maintanance::orbit==$orbit\n";
print "In main::maintanance::owner==$name\n";
print "Going to cantMaintain\n";
      my $shortage = 
       $Planet->[$system][$orbit]->cantMaintain($pl_ref->{'Industry'});
      my $stdupdate = 
	"UPDATE SINGLE Ship SET HomePortStar='' AND HomeportOrbit=0 ";
      $stdquery = " where GameNo= " .$GN. " AND Faction='".
	$name." AND HomePortStar= '".$system.
	"' AND HomeportOrbit=".$orbit ." AND ShipType='";
      while ($shortage>0) {
         if (returnDBrow("SELECT * from Ship ".$stdquery."Frigates'")>0){
             operate_on_DB($stdupdate.$stdquery."Frigates'");
             $Planet->[$system][$orbit]->deal_with_dead_ships(1); 
             $shortage-=1;
         } elsif (returnDBrow("SELECT * from Ship".$stdquery."Battleship'")>0){
             operate_on_DB($stdupdate.$stdquery."Battleship'");
             $Planet->[$system][$orbit]->deal_with_dead_ships(2); 
             $shortage-=2;
         } elsif (returnDBrow("SELECT * from Ship".$stdquery."Transport'")>0){
             operate_on_DB($stdupdate.$stdquery."Transport'");
             $Planet->[$system][$orbit]->deal_with_dead_ships(1); 
             $shortage-=1;
         }  else {
	     ## bad. ADD ERROR LOG entry.
             ## break;
		;
         }         
      }
	## changed by RKS.
        ## $Planet->[$system][$orbit]->remove_bases($shortage) ;
       $Planet->[$system][$orbit]->scrapBases($shortage) ;
   }
   $sth50->finish;
}

sub writeToDatabase {
    ### 25 systems, hardcoded. If changing number of systems change this number
print "In writeToDatabase\n";
    my $maxOrbits = 5;
    my $maxStars = 25;
    my $i=1; 
    my $j=1;
    my $q='';
    my $factionName = '';

############################################################

    for ($i=1; $i <= $maxStars; $i++) {

       ## I dont think $length is doing what sera intented. DEBUG ME. RKS.
       ## my $length = (@Planet[$i] + 0);
       ## code below doesn't work-sera's. $length cant get array length from
       ## 2d array. RKS. moved to while loop.
       ## for ($j=0; $j < $length; $j++) 

       $j = 1;

       while ( $j <= $maxOrbits ) {
	## print "planetExists($i,$j)\n";
       if ( planetExists($i, $j) == 1 ) {

          if ( $Planet->[$i][$j]->ownerName() ) {
              $factionName = $Planet->[$i][$j]->ownerName() 
          }
          else { $factionName = "" ; }
   
	## print "for loop system: $i orbit: $j while loop: ";
	## print " factionName: $factionName GameNo: $GN\n";

## LastTurnMaint has prblem during compile. Not writing DB
## Solved. changed LastTurnMaint type to real in dB. RKS.
            $q="UPDATE Planet SET OwnerFactionName ='" . 
	       $factionName . "', TotalFactories=" .
	       checkDef( $Planet->[$i][$j]->numFac() ) . ", TotalMines=" .
	       checkDef( $Planet->[$i][$j]->numMines() ) . ", RawMaterials=" . 
 	       checkDef( $Planet->[$i][$j]->RawMat() ) . ", NoBases=" . 
  	       checkDef( $Planet->[$i][$j]->Bases() ) . ", LastTurnMaint= " .
  	       checkDef( $Planet->[$i][$j]->maint() ) . ", Troops= " . 
  	       checkDef( $Planet->[$i][$j]->Troops() ) . ", SecurityLevel= " . 
  	       checkDef( $Planet->[$i][$j]->security() ) ." WHERE GameNo= " . 
	       $GN . " AND SysNo= " . $i . " AND Orbit= " . $j;
            $sth= $dbh->prepare($q);
            $sth->execute;
            $sth->finish;

       } ## end of if $planetExists
       $j++;
       } ## end of while loop
	## print "\n";

   } ## end of for loop

############################################################

  $q = "UPDATE GameStatus SET LastShipNo=".$SN." WHERE GameNo=".$GN;
  operate_on_DB($q);
            
} ## end of function

sub planetExists {
    my ($s, $o) = (@_);
    my $bool = 0;
    my $q= "SELECT * from Planet where SysNo=" .$s. " AND Orbit=" . $o .
	" AND GameNo=" . $GN;
    my $sth= $dbh->prepare($q);
    $sth->execute;
    my $rows = $sth->rows;
    $sth->finish;
	## print "planetExists system: $s orbit: $o rows: $rows";
    if ( $rows > 0 ) {
	$bool = 1;
    }
	## print " return: $bool\n";
return $bool;
}

sub checkDef {
   my ($value) = (@_);
   if ( $value ) {
      return $value;
   }
   else {
   return 0;
   }
}

1;


