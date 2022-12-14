extends CharacterBody2D


const SPEED = 300.0

func _ready():
	$Networking/MultiplayerSync.set_multiplayer_authority(str(name).to_int())
	_change_spawn()
	$Nickname.text = str(name)
	
func _is_local_authority():
	return $Networking/MultiplayerSync.get_multiplayer_authority() == multiplayer.get_unique_id()

func _physics_process(delta):
	
	if _is_local_authority():
		var direction = Input.get_axis("ui_left", "ui_right")
		var directionY = Input.get_axis("ui_up", "ui_down")
		
		if direction:
			velocity.x = direction * SPEED
		else:
			velocity.x = move_toward(velocity.x, 0, SPEED)
		
		if directionY:
			velocity.y = directionY * SPEED
		else:
			velocity.y = move_toward(velocity.y, 0, SPEED)

		move_and_slide()
		
		$Networking.sync_position = position
		
	else:
		if not $Networking.processed_position:
			position = $Networking.sync_position
			$Networking.processed_position = true
		

func _change_spawn():
	var spawn_x = randi_range(200,400)
	var spawn_y = randi_range(200,400)
	position = Vector2(spawn_x,spawn_y)	
	$Networking.sync_position = position
		
		
		
		
		
		
		
		
