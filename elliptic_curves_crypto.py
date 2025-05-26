import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math

class EllipticCurve:
    """Classe pour représenter une courbe elliptique y² = x³ + ax + b (mod p)"""
    
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        
        # Vérifier que la courbe est non-singulière
        discriminant = (4 * a**3 + 27 * b**2) % p
        if discriminant == 0:
            raise ValueError("Courbe singulière (discriminant = 0)")
    
    def is_on_curve(self, x, y):
        """Vérifie si un point (x,y) est sur la courbe"""
        if x is None and y is None:  # Point à l'infini
            return True
        return (y**2) % self.p == (x**3 + self.a * x + self.b) % self.p
    
    def point_addition(self, P, Q):
        """Addition de deux points sur la courbe elliptique"""
        # Point à l'infini
        if P is None:
            return Q
        if Q is None:
            return P
        
        x1, y1 = P
        x2, y2 = Q
        
        # Points opposés
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None  # Point à l'infini
        
        # Même point (doublement)
        if x1 == x2 and y1 == y2:
            s = (3 * x1**2 + self.a) * self.mod_inverse(2 * y1, self.p) % self.p
        else:
            # Points différents
            s = (y2 - y1) * self.mod_inverse(x2 - x1, self.p) % self.p
        
        x3 = (s**2 - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def point_multiplication(self, k, P):
        """Multiplication scalaire k*P"""
        if k == 0 or P is None:
            return None
        
        if k < 0:
            # Négatif: calculer -k*P puis prendre l'opposé
            k = -k
            result = self.point_multiplication(k, P)
            if result is None:
                return None
            return (result[0], (-result[1]) % self.p)
        
        result = None
        addend = P
        
        while k:
            if k & 1:
                result = self.point_addition(result, addend)
            addend = self.point_addition(addend, addend)
            k >>= 1
        
        return result
    
    def mod_inverse(self, a, m):
        """Inverse modulaire de a modulo m"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError("Inverse modulaire n'existe pas")
        return x % m
    
    def get_all_points(self):
        """Génère tous les points de la courbe"""
        points = [None]  # Point à l'infini
        
        for x in range(self.p):
            y_squared = (x**3 + self.a * x + self.b) % self.p
            for y in range(self.p):
                if (y * y) % self.p == y_squared:
                    points.append((x, y))
        
        return points
    
    def point_order(self, P):
        """Calcule l'ordre d'un point P"""
        if P is None:
            return 1
        
        current = P
        order = 1
        
        while current is not None:
            current = self.point_addition(current, P)
            order += 1
            if order > self.p * 2:  # Sécurité
                break
        
        return order

class EllipticCurveGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Courbes Elliptiques - Cryptographie")
        self.root.geometry("1100x750")
        
        self.curve = None
        self.points = []
        
        # Couleurs
        self.root.configure(bg='#f0f0f0')
        
        self.setup_ui()
        
        # Charger une courbe par défaut
        self.create_curve()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titre
        title_label = ttk.Label(main_frame, text="COURBES ELLIPTIQUES - CRYPTOGRAPHIE", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Configuration de la courbe
        curve_frame = ttk.LabelFrame(main_frame, text="📊 Configuration de la courbe", padding="15")
        curve_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(curve_frame, text="Équation: y² = x³ + ax + b (mod p)", 
                 font=("Arial", 11, "italic")).grid(row=0, column=0, columnspan=6, pady=(0, 15))
        
        # Paramètres sur une ligne
        ttk.Label(curve_frame, text="a =").grid(row=1, column=0, padx=(0, 5))
        self.a_var = tk.StringVar(value="2")
        ttk.Entry(curve_frame, textvariable=self.a_var, width=8).grid(row=1, column=1, padx=(0, 15))
        
        ttk.Label(curve_frame, text="b =").grid(row=1, column=2, padx=(0, 5))
        self.b_var = tk.StringVar(value="3")
        ttk.Entry(curve_frame, textvariable=self.b_var, width=8).grid(row=1, column=3, padx=(0, 15))
        
        ttk.Label(curve_frame, text="p =").grid(row=1, column=4, padx=(0, 5))
        self.p_var = tk.StringVar(value="17")
        ttk.Entry(curve_frame, textvariable=self.p_var, width=8).grid(row=1, column=5, padx=(0, 15))
        
        ttk.Button(curve_frame, text="🔄 Créer courbe", 
                  command=self.create_curve).grid(row=1, column=6, padx=(10, 0))
        
        # Exemples de courbes
        examples_frame = ttk.Frame(curve_frame)
        examples_frame.grid(row=2, column=0, columnspan=7, pady=(10, 0))
        
        ttk.Label(examples_frame, text="Exemples:").grid(row=0, column=0, padx=(0, 10))
        ttk.Button(examples_frame, text="secp256k1", 
                  command=lambda: self.load_example(1, 0, 23)).grid(row=0, column=1, padx=5)
        ttk.Button(examples_frame, text="Curve25519", 
                  command=lambda: self.load_example(-1, 1, 19)).grid(row=0, column=2, padx=5)
        ttk.Button(examples_frame, text="Simple", 
                  command=lambda: self.load_example(2, 3, 17)).grid(row=0, column=3, padx=5)
        
        # Frame gauche - Opérations
        left_frame = ttk.LabelFrame(main_frame, text="🔧 Opérations", padding="15")
        left_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        
        # Addition de points
        ttk.Label(left_frame, text="➕ Addition P + Q:", 
                 font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(left_frame, text="P(x,y) =").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.p1_var = tk.StringVar(value="(6, 3)")
        ttk.Entry(left_frame, textvariable=self.p1_var, width=18).grid(row=1, column=1, padx=(5, 0), pady=2)
        
        ttk.Label(left_frame, text="Q(x,y) =").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.p2_var = tk.StringVar(value="(10, 6)")
        ttk.Entry(left_frame, textvariable=self.p2_var, width=18).grid(row=2, column=1, padx=(5, 0), pady=2)
        
        ttk.Button(left_frame, text="🧮 Calculer P + Q", 
                  command=self.add_points).grid(row=3, column=0, columnspan=2, pady=15)
        
        # Multiplication scalaire
        ttk.Label(left_frame, text="✖️ Multiplication k*P:", 
                 font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        
        ttk.Label(left_frame, text="k =").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.k_var = tk.StringVar(value="3")
        ttk.Entry(left_frame, textvariable=self.k_var, width=18).grid(row=5, column=1, padx=(5, 0), pady=2)
        
        ttk.Label(left_frame, text="P(x,y) =").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.p_mult_var = tk.StringVar(value="(6, 3)")
        ttk.Entry(left_frame, textvariable=self.p_mult_var, width=18).grid(row=6, column=1, padx=(5, 0), pady=2)
        
        ttk.Button(left_frame, text="🧮 Calculer k*P", 
                  command=self.multiply_point).grid(row=7, column=0, columnspan=2, pady=15)
        
        # Ordre d'un point
        ttk.Label(left_frame, text="📏 Ordre d'un point:", 
                 font=("Arial", 10, "bold")).grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        
        ttk.Label(left_frame, text="P(x,y) =").grid(row=9, column=0, sticky=tk.W, pady=2)
        self.p_order_var = tk.StringVar(value="(6, 3)")
        ttk.Entry(left_frame, textvariable=self.p_order_var, width=18).grid(row=9, column=1, padx=(5, 0), pady=2)
        
        ttk.Button(left_frame, text="📊 Calculer ordre", 
                  command=self.calculate_order).grid(row=10, column=0, columnspan=2, pady=15)
        
        # Boutons utilitaires
        utils_frame = ttk.LabelFrame(left_frame, text="🛠️ Utilitaires", padding="10")
        utils_frame.grid(row=11, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        ttk.Button(utils_frame, text="📋 Tous les points", 
                  command=self.show_all_points).grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(utils_frame, text="📈 Graphique courbe", 
                  command=self.plot_curve).grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(utils_frame, text="🔍 Vérifier point", 
                  command=self.verify_point).grid(row=2, column=0, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(utils_frame, text="🗑️ Effacer résultats", 
                  command=self.clear_results).grid(row=3, column=0, pady=5, sticky=(tk.W, tk.E))
        
        utils_frame.columnconfigure(0, weight=1)
        
        # Frame droite - Résultats
        results_frame = ttk.LabelFrame(main_frame, text="📊 Résultats et Informations", padding="15")
        results_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.results_text = scrolledtext.ScrolledText(results_frame, width=60, height=25, font=("Consolas", 10))
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configuration du redimensionnement
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def load_example(self, a, b, p):
        """Charge un exemple de courbe"""
        self.a_var.set(str(a))
        self.b_var.set(str(b))
        self.p_var.set(str(p))
        self.create_curve()
    
    def log_result(self, message):
        """Ajoute un message aux résultats"""
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
    
    def clear_results(self):
        """Efface tous les résultats"""
        self.results_text.delete(1.0, tk.END)
    
    def create_curve(self):
        """Crée une nouvelle courbe elliptique"""
        try:
            a = int(self.a_var.get())
            b = int(self.b_var.get())
            p = int(self.p_var.get())
            
            if p < 3:
                raise ValueError("p doit être ≥ 3")
            
            self.curve = EllipticCurve(a, b, p)
            self.points = self.curve.get_all_points()
            
            self.log_result("="*60)
            self.log_result(f"🆕 NOUVELLE COURBE CRÉÉE")
            self.log_result(f"Équation: y² = x³ + {a}x + {b} (mod {p})")
            self.log_result(f"Discriminant: {(4 * a**3 + 27 * b**2) % p}")
            self.log_result(f"Nombre total de points: {len(self.points)}")
            
            # Afficher les premiers points
            display_points = []
            for i, point in enumerate(self.points[:15]):
                if point is None:
                    display_points.append("∞")
                else:
                    display_points.append(f"({point[0]},{point[1]})")
            
            self.log_result(f"Premiers points: {', '.join(display_points)}")
            if len(self.points) > 15:
                self.log_result(f"... et {len(self.points) - 15} autres points")
            self.log_result("="*60)
            
        except ValueError as e:
            messagebox.showerror("❌ Erreur", str(e))
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la création: {e}")
    
    def parse_point(self, point_str):
        """Parse une chaîne point au format (x,y)"""
        point_str = point_str.strip()
        if point_str.lower() in ["none", "inf", "∞", "(∞)", "infini"]:
            return None
        
        point_str = point_str.strip("()")
        coords = point_str.split(",")
        if len(coords) != 2:
            raise ValueError("Format incorrect. Utilisez (x,y)")
        
        x, y = int(coords[0].strip()), int(coords[1].strip())
        return (x, y)
    
    def add_points(self):
        """Addition de deux points"""
        if not self.curve:
            messagebox.showerror("❌ Erreur", "Créez d'abord une courbe")
            return
        
        try:
            P = self.parse_point(self.p1_var.get())
            Q = self.parse_point(self.p2_var.get())
            
            # Vérifier que les points sont sur la courbe
            if P and not self.curve.is_on_curve(P[0], P[1]):
                messagebox.showerror("❌ Erreur", f"Le point P {P} n'est pas sur la courbe")
                return
            if Q and not self.curve.is_on_curve(Q[0], Q[1]):
                messagebox.showerror("❌ Erreur", f"Le point Q {Q} n'est pas sur la courbe")
                return
            
            result = self.curve.point_addition(P, Q)
            
            P_str = "∞" if P is None else f"({P[0]}, {P[1]})"
            Q_str = "∞" if Q is None else f"({Q[0]}, {Q[1]})"
            result_str = "∞" if result is None else f"({result[0]}, {result[1]})"
            
            self.log_result(f"➕ ADDITION: {P_str} + {Q_str} = {result_str}")
            
            # Vérification
            if result and self.curve.is_on_curve(result[0], result[1]):
                self.log_result("   ✅ Résultat vérifié sur la courbe")
            elif result is None:
                self.log_result("   ✅ Point à l'infini")
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de l'addition: {e}")
    
    def multiply_point(self):
        """Multiplication scalaire"""
        if not self.curve:
            messagebox.showerror("❌ Erreur", "Créez d'abord une courbe")
            return
        
        try:
            k = int(self.k_var.get())
            P = self.parse_point(self.p_mult_var.get())
            
            if P and not self.curve.is_on_curve(P[0], P[1]):
                messagebox.showerror("❌ Erreur", f"Le point P {P} n'est pas sur la courbe")
                return
            
            result = self.curve.point_multiplication(k, P)
            
            P_str = "∞" if P is None else f"({P[0]}, {P[1]})"
            result_str = "∞" if result is None else f"({result[0]}, {result[1]})"
            
            self.log_result(f"✖️ MULTIPLICATION: {k} × {P_str} = {result_str}")
            
            # Étapes intermédiaires pour k petit
            if abs(k) <= 10 and P is not None:
                self.log_result("   📋 Étapes:")
                current = None
                for i in range(1, abs(k) + 1):
                    current = self.curve.point_addition(current, P)
                    current_str = "∞" if current is None else f"({current[0]}, {current[1]})"
                    self.log_result(f"      {i}P = {current_str}")
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la multiplication: {e}")
    
    def calculate_order(self):
        """Calcule l'ordre d'un point"""
        if not self.curve:
            messagebox.showerror("❌ Erreur", "Créez d'abord une courbe")
            return
        
        try:
            P = self.parse_point(self.p_order_var.get())
            
            if P and not self.curve.is_on_curve(P[0], P[1]):
                messagebox.showerror("❌ Erreur", f"Le point P {P} n'est pas sur la courbe")
                return
            
            order = self.curve.point_order(P)
            P_str = "∞" if P is None else f"({P[0]}, {P[1]})"
            
            self.log_result(f"📏 ORDRE du point {P_str}: {order}")
            
            # Montrer quelques multiples
            if P is not None and order <= 20:
                self.log_result("   📋 Multiples:")
                current = None
                for i in range(1, order + 1):
                    current = self.curve.point_addition(current, P)
                    if current is None:
                        self.log_result(f"      {i}P = ∞")
                        break
                    else:
                        self.log_result(f"      {i}P = ({current[0]}, {current[1]})")
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors du calcul d'ordre: {e}")
    
    def verify_point(self):
        """Vérifie si un point est sur la courbe"""
        if not self.curve:
            messagebox.showerror("❌ Erreur", "Créez d'abord une courbe")
            return
        
        # Demander le point à vérifier
        point_str = tk.simpledialog.askstring("Vérification", "Entrez le point à vérifier (x,y):")
        if not point_str:
            return
        
        try:
            point = self.parse_point(point_str)
            if point is None:
                self.log_result("🔍 VÉRIFICATION: ∞ est toujours sur la courbe ✅")
                return
            
            x, y = point
            on_curve = self.curve.is_on_curve(x, y)
            
            # Calculs détaillés
            left_side = (y**2) % self.curve.p
            right_side = (x**3 + self.curve.a * x + self.curve.b) % self.curve.p
            
            self.log_result(f"🔍 VÉRIFICATION du point ({x}, {y}):")
            self.log_result(f"   y² mod {self.curve.p} = {y}² mod {self.curve.p} = {left_side}")
            self.log_result(f"   x³+ax+b mod {self.curve.p} = {x}³+{self.curve.a}×{x}+{self.curve.b} mod {self.curve.p} = {right_side}")
            
            if on_curve:
                self.log_result(f"   ✅ {left_side} = {right_side} → Point SUR la courbe")
            else:
                self.log_result(f"   ❌ {left_side} ≠ {right_side} → Point PAS sur la courbe")
                
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la vérification: {e}")
    
    def show_all_points(self):
        """Affiche tous les points de la courbe"""
        if not self.curve:
            messagebox.showerror("❌ Erreur", "Créez d'abord une courbe")
            return
        
        self.log_result(f"📋 TOUS LES POINTS (Total: {len(self.points)}):")
        self.log_result("-" * 60)
        
        # Grouper par ligne de 6 points
        line = []
        for i, point in enumerate(self.points):
            if point is None:
                line.append("∞".center(8))
            else:
                line.append(f"({point[0]},{point[1]})".center(8))
            
            if len(line) == 6 or i == len(self.points) - 1:
                self.log_result(" ".join(line))
                line = []
        
        self.log_result("-" * 60)
    
    def plot_curve(self):
        """Affiche le graphique de la courbe avec tkinter Canvas"""
        if not self.curve:
            messagebox.showerror("❌ Erreur", "Créez d'abord une courbe")
            return
        
        # Nouvelle fenêtre pour le graphique
        plot_window = tk.Toplevel(self.root)
        plot_window.title(f"Courbe: y² = x³ + {self.curve.a}x + {self.curve.b} (mod {self.curve.p})")
        plot_window.geometry("800x700")
        plot_window.configure(bg='white')
        
        # Frame pour les contrôles
        control_frame = ttk.Frame(plot_window, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Informations sur la courbe
        info_label = ttk.Label(control_frame, 
                              text=f"Courbe: y² = x³ + {self.curve.a}x + {self.curve.b} (mod {self.curve.p}) | Points: {len(self.points)}")
        info_label.pack()
        
        # Canvas pour le graphique
        canvas_frame = ttk.Frame(plot_window)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(canvas_frame, bg='white', bd=2, relief='sunken')
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Attendre que le canvas soit affiché pour obtenir ses dimensions
        plot_window.update()
        
        # Dimensions du canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width, canvas_height = 760, 600
        
        # Marges
        margin = 60
        plot_width = canvas_width - 2 * margin
        plot_height = canvas_height - 2 * margin
        
        # Échelle
        max_coord = max(self.curve.p - 1, 1)
        scale_x = plot_width / max_coord
        scale_y = plot_height / max_coord
        
        def to_canvas_coords(x, y):
            """Convertit les coordonnées mathématiques en coordonnées canvas"""
            canvas_x = margin + x * scale_x
            canvas_y = margin + (max_coord - y) * scale_y  # Inverser Y
            return canvas_x, canvas_y
        
        # Dessiner les axes
        # Axe X
        canvas.create_line(margin, margin + plot_height, 
                          margin + plot_width, margin + plot_height,
                          fill='gray', width=2)
        # Axe Y
        canvas.create_line(margin, margin, 
                          margin, margin + plot_height,
                          fill='gray', width=2)
        
        # Graduations X
        for i in range(0, self.curve.p, max(1, self.curve.p // 10)):
            x, y = to_canvas_coords(i, 0)
            canvas.create_line(x, y - 5, x, y + 5, fill='gray')
            canvas.create_text(x, y + 15, text=str(i), font=('Arial', 8))
        
        # Graduations Y
        for i in range(0, self.curve.p, max(1, self.curve.p // 10)):
            x, y = to_canvas_coords(0, i)
            canvas.create_line(x - 5, y, x + 5, y, fill='gray')
            canvas.create_text(x - 15, y, text=str(i), font=('Arial', 8))
        
        # Labels des axes
        canvas.create_text(margin + plot_width/2, margin + plot_height + 40, 
                          text='x', font=('Arial', 12, 'bold'))
        canvas.create_text(margin - 40, margin + plot_height/2, 
                          text='y', font=('Arial', 12, 'bold'))
        
        # Dessiner la grille
        for i in range(0, self.curve.p + 1, max(1, self.curve.p // 20)):
            # Lignes verticales
            x, y1 = to_canvas_coords(i, 0)
            x, y2 = to_canvas_coords(i, max_coord)
            canvas.create_line(x, y1, x, y2, fill='lightgray', width=1)
            
            # Lignes horizontales
            x1, y = to_canvas_coords(0, i)
            x2, y = to_canvas_coords(max_coord, i)
            canvas.create_line(x1, y, x2, y, fill='lightgray', width=1)
        
        # Dessiner les points de la courbe
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
        finite_points = [p for p in self.points if p is not None]
        
        for i, (x, y) in enumerate(finite_points):
            canvas_x, canvas_y = to_canvas_coords(x, y)
            color = colors[i % len(colors)]
            
            # Point principal
            canvas.create_oval(canvas_x - 4, canvas_y - 4, 
                             canvas_x + 4, canvas_y + 4,
                             fill=color, outline='black', width=2)
            
            # Étiquette avec coordonnées
            if len(finite_points) <= 30:  # Éviter l'encombrement
                canvas.create_text(canvas_x + 12, canvas_y - 8, 
                                 text=f'({x},{y})', 
                                 font=('Arial', 8), fill=color)
        
        # Légende
        legend_y = 20
        canvas.create_text(canvas_width - 100, legend_y, 
                          text=f'Points sur la courbe: {len(finite_points)}', 
                          font=('Arial', 10, 'bold'))
        
        # Point à l'infini
        if None in self.points:
            canvas.create_text(canvas_width - 100, legend_y + 20, 
                              text='+ Point à l\'infini (∞)', 
                              font=('Arial', 9), fill='darkred')
        
        # Boutons dans la fenêtre graphique
        button_frame = ttk.Frame(plot_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="🔄 Actualiser", 
                  command=lambda: self.refresh_plot(canvas, plot_window)).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="💾 Sauvegarder info", 
                  command=lambda: self.save_curve_info()).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="❌ Fermer", 
                  command=plot_window.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Afficher des statistiques
        self.log_result("📊 GRAPHIQUE GÉNÉRÉ:")
        self.log_result(f"   Courbe: y² = x³ + {self.curve.a}x + {self.curve.b} (mod {self.curve.p})")
        self.log_result(f"   Points finis affichés: {len(finite_points)}")
        self.log_result(f"   Domaine: [0, {self.curve.p-1}] × [0, {self.curve.p-1}]")
    
    def refresh_plot(self, canvas, window):
        """Actualise le graphique"""
        window.destroy()
        self.plot_curve()
    
    def save_curve_info(self):
        """Sauvegarde les informations de la courbe"""
        if not self.curve:
            return
        
        info = f"""COURBE ELLIPTIQUE - RAPPORT
===============================
Équation: y² = x³ + {self.curve.a}x + {self.curve.b} (mod {self.curve.p})
Discriminant: {(4 * self.curve.a**3 + 27 * self.curve.b**2) % self.curve.p}
Nombre de points: {len(self.points)}

POINTS DE LA COURBE:
"""
        for i, point in enumerate(self.points):
            if point is None:
                info += f"{i+1:2d}. ∞ (Point à l'infini)\n"
            else:
                info += f"{i+1:2d}. ({point[0]:2d}, {point[1]:2d})\n"
        
        # Sauvegarder dans un fichier
        try:
            filename = f"courbe_{self.curve.a}_{self.curve.b}_{self.curve.p}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(info)
            self.log_result(f"💾 Informations sauvegardées dans: {filename}")
            messagebox.showinfo("✅ Succès", f"Fichier sauvegardé: {filename}")
        except Exception as e:
            self.log_result(f"❌ Erreur sauvegarde: {e}")

# Ajouter le module pour les dialogues
import tkinter.simpledialog

def main():
    root = tk.Tk()
    app = EllipticCurveGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()