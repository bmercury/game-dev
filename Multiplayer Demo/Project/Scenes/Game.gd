extends Node

var character_scene = preload("res://Character.tscn")

# Called when the node enters the scene tree for the first time.
func _enter_tree():
	if Global.is_server or "--server" in OS.get_cmdline_args():
		init_networking(true)
	else:
		init_networking(false)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func init_networking(is_server):
	var peer = ENetMultiplayerPeer.new()
	
	if is_server:
		multiplayer.peer_connected.connect(self.create_player)
		multiplayer.peer_disconnected.connect(self.destroy_player)
		peer.create_server(Global.DEFAULT_PORT)
		print("Server listening on ", Global.DEFAULT_PORT)
	else:
		peer.create_client("localhost", Global.DEFAULT_PORT)
		
	multiplayer.set_multiplayer_peer(peer)
	$PlayerName.text = str(get_tree().get_multiplayer().get_unique_id())

func create_player(id: int) -> void :
	var character_instance = character_scene.instantiate()
	character_instance.name = str(id)
	$Players.add_child(character_instance)
	$PlayerName.text = str(id)
	print("Player ", str(id), " joined")
	
func destroy_player(id: int) -> void:
	$Players.get_node(str(id)).queue_free()
	print("Player ", str(id), " left")
