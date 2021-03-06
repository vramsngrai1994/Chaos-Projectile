"""
.. module:: rendersystem
   :Platform: Unix, Windows
   :Synopsis: Render system
"""

import pygame
import events
import pyscroll


class RenderSystem(object):
    """Render system.
    
    :Attributes:
        - *evManager*: event manager
        - *world*: game world
        - *screen*: game screen
    """

    def __init__(self, event_manager, world):
        """
        :param event_manager: event Manager
        :type event_manager: events.EventManager
        :param world: game world
        :type world: gameWorld.GameWorld
        """
        self.world = world
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        #Set game screen
        self.screen = world.screen
        w, h = world.screen.get_size()
        #Create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(self.world.level.map_data,
                                                   (w, h),
                                                   clamp_camera=False)
        #The sprite should to be on top of layer named "decoration behind"
        #Find layer number of the layer named "decoration behind"
        self.render_layer = 0
        for layer_index in range(len(self.world.level.tmx_data.layers)):
            if self.world.level.tmx_data.layers[layer_index].name == "decoration behind":
                self.render_layer = layer_index
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer,
                                            default_layer=self.render_layer)
        #Add other sprites
        #for image in self.world.appearance:
        #    self.group.add(self.world.appearance[image])

    def notify(self, event):
        """Notify, when event occurs and stop CPUSpinner when it's quit event. 
        
        :param event: occurred event
        :type event: events.Event
        """
        if isinstance(event, events.TickEvent):
            self.draw(event.dt)
        if isinstance(event, events.ResizeWindowEvent):
            self.resize(event.width, event.height)

    def update(self):
        """Updates group, so new entities can be added and dead removed.
        
        Every update the default layer,where all game entities will be drawn, should be cleaned and reassigned.
        """
        self.group.remove_sprites_of_layer(self.render_layer)
        #Add all game components
        for image in self.world.appearance.itervalues():
            if image.play_animation:
                self.group.add(image)

    def draw(self, dt):
        """Draw everything on the screen.
        
        :param dt: CPU tick
        :type dt: int
        """
        self.update()
        self.group.update(dt)
        #Center the map/screen on the single player
        self.group.center(self.world.collider[self.world.player].center)
        #Draw the level and all other sprites
        self.group.draw(self.screen)
        pygame.display.flip()

    def resize(self, w, h):
        """Resize game window.
        
        :param w: new width in pixels
        :type w: int
        :param h: new height in pixels
        :type h: int
        """
        pygame.display.set_mode((w, h), pygame.RESIZABLE)
        self.map_layer.set_size((w, h))
