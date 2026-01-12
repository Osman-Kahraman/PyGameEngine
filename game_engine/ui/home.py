import repackage

from images.init import *
repackage.up()
from gameMotors import *

class Window:
    def __init__(self, screen: pygame.Surface):
        self.surface = screen
        self.surface_sizes = self.surface.get_rect().size
        self.screen_mid = tuple(np.array(self.surface_sizes) // 2)
        self.cursor_pos = self.screen_mid
        self.cursor_bool = True
        self.cursor = image_.normalCursor
        self.file_action = False
        self.command = "home_start"
        self.blur_screen = pygame.Surface((1366, 768)).convert_alpha()

        #-Requested News------------------------------------------------------------
        with open("game_engine/news.txt", "r", encoding = "utf-8") as file:
            self.news = "".join(file.readlines())
        #---------------------------------------------------------------------------

    def update(self):
        pygame_.get()

        #-Display Event---------------------------------------------------------------------------------------------------------------------------------------------------------
        for event in pygame_.event:
            e_type = event.type
            self.cursor_bool = False if e_type == 1 or e_type == 17 else True

            if e_type == pygame.QUIT:
                self.cursor_bool = False
                self.command = "quit"

            if e_type == pygame.MOUSEMOTION:
                self.cursor_pos = event.pos
                if any([
                    UI.listen("fileActionButton") == "waked_up", 
                    UI.listen("action_1") == "waked_up", 
                    UI.listen("action_2") == "waked_up"
                    ]):
                    self.cursor = image_.choosingCursor
                else:
                    self.cursor = image_.normalCursor
            elif e_type == pygame.MOUSEBUTTONDOWN:
                e_button = event.button

                if e_button == 1: 
                    self.cursor = image_.normalCursorL
                elif e_button == 3:
                    self.cursor = image_.normalCursorR
            elif e_type == pygame.MOUSEBUTTONUP: 
                self.cursor = image_.normalCursor if self.cursor == image_.normalCursorL or self.cursor == image_.normalCursorR else image_.choosingCursor
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #-Background Layout---------
        self.surface.fill((30, 30, 30)) #Dark Gray
        #---------------------------

        #-UI Settings----------------------------------------------------------------------------------------------------------------------------------------------
        a = UI.window("news", (20, 70), (1356 // 2, 400), (30, 30, 30), 2)
        self.surface.blit(a[0], a[1])
        UI.text(self.news, 18, (15, 10), (200, 200, 200), win_name = "news", font = "segoescript")
        b = UI.window("foo", (1356 // 2 + 40, 70), (1356 // 2 - 40, 200), (30, 30, 30), 2)
        self.surface.blit(b[0], b[1])
        UI.text(
        """Lorem ipsum dolor sit amet, sint salutatus ius ut. Et purto molestie pro. Legendos recusabo intellegat ea ius, possit facilis torquatos cu quo. Pro quas veritus detraxit cu.

        Omnes audire torquatos et eos. Partem tritani sit id. Omnes percipit democritum eu his. His nobis dolores et, pri nihil intellegat cu, duis omnesque an per.

        Agam referrentur cum cu, tritani invidunt abhorreant ex eum. No nec eruditi appetere elaboraret. Has at nostro saperet neglegentur. Cum novum iisque delicatissimi te, ad pro dicam periculis. Id eos ignota propriae, ne eam invenire iudicabit, eu vis soluta doctus singulis.

        Nullam vivendum quo ei, at vulputate vituperata sea. Vivendo splendide quo in. Amet disputationi vim et, ei sea feugiat voluptatum adversarium, reque primis malorum cum te. No mea praesent hendrerit complectitur. Sed erroribus imperdiet an. At habeo assum fabellas pro. Pro ad mollis laoreet legendos, ei vel agam libris verear, ut usu quot salutandi.

        Ius partiendo petentium ne, ad quo purto justo, usu et error conceptam persequeris. Indoctum explicari cum an, vim ei erroribus voluptatibus. Quem feugiat sea at, utinam eligendi eum ex, wisi saepe vis ei. Pri vivendo petentium scriptorem ne, no sed inani persecuti. Pro in lucilius definiebas, vix iudico decore et. Est essent assueverit ex, minimum officiis est ne, at nam nibh nonumy.""", 18, (0, 0), (200, 200, 200), "foo") 
        c = UI.window("bar", (20, 480), (260, 60), (30, 30, 30), 2)
        self.surface.blit(c[0], c[1])
        UI.text("Lorem ipsum dolor sit amet, sint salutatus ius ut.", 19, (5, 5), (200, 200, 200), "bar")
        d = UI.window("e-mail", (300, 480), (400, 60), (30, 30, 30), 2)
        self.surface.blit(d[0], d[1])
        UI.text("o_kahraman@outlook.com :)", 19, (5, 5), (200, 200, 200), "e-mail")
        e = UI.window("casio", (1356 // 2 + 40, 280), (638, 359), (30, 30, 30), 2)
        self.surface.blit(e[0], e[1])
        UI.add_images({(0, 0): image_.casio}, "casio")

        if self.file_action:
            top_navbar_action_surf, top_navbar_action_coor = UI.window("top_navbar_action", (10, 40), (100, 300), (50, 50, 50), 1)
            
            self.blur_screen.fill((70, 70, 70, 128))
            self.surface.blit(self.blur_screen, (0, 0))
            
            UI.window("action_1", (2, 2), (90, 20), (50, 50, 50), "button", win_name = "top_navbar_action")
            UI.text("New...", 14, (3, 3), (200, 200, 200), win_name = "action_1")
            UI.window("action_2", (2, 23), (90, 20), (50, 50, 50), "button", win_name = "top_navbar_action")
            UI.text("Open...", 14, (3, 3), (200, 200, 200), win_name = "action_2")
            try:
                self.surface.blit(top_navbar_action_surf, top_navbar_action_coor)
            except:
                if top_navbar_action_surf.item_coords == (2, 2):
                    pass
                elif top_navbar_action_surf.item_coords == (2, 23):
                    self.command = "game_start"

        top_navbar_surf, top_navbar_coor = UI.window("top_navbar", (-10, 0), (1386, 40), (0, 0, 0), 1)
        UI.window("fileActionButton", (15, 8), (70, 20), (0, 0, 0), "button", win_name = "top_navbar")
        UI.text("File", 15, (3, 0), (200, 200, 200), win_name = "fileActionButton", font = "impact")
        UI.window("versionTextButton", (self.surface_sizes[0] - 100, 8), (100, 20), (0, 0, 0), win_name = "top_navbar")
        UI.text("Work in Progress", 15, (3, 0), (200, 200, 200), win_name = "versionTextButton", font = "impact")
        try:
            self.surface.blit(top_navbar_surf, top_navbar_coor)
        except TypeError:
            if top_navbar_surf.item_coords == (15, 8):
                self.file_action = False if self.file_action else True
            else:
                pass

        self.surface.blit(image_.pygameSnake, (self.screen_mid[0] - (image_.pygameSnake.get_size()[0] // 2), 0))
        #---------------------------------------------------------------------------------------------------------------------------------------------------------

        #-Cursor----------------------------
        if self.cursor_bool:
            self.surface.blit(self.cursor, self.cursor_pos)
        #-----------------------------------

        return self.command