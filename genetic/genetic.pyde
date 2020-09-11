# Gen sayısı. Atılacak Adım sayısı
NUMBER_OF_GENES = 750
# Birey sayısı
NUMBER_OF_ENTITIES = 200
# Adım uzunluğu
STEP_MAG = 15
# Mutasyon olasılığı %
MUTATION_RATE = 0
# Jenerasyon. Değiştirmeyin
GENERATION = 0
# Frame. Değiştirmeyin
FRAME = 0

# Bireyler dizisi
entities = []
# Hedef
target = None
# Engeller dizisi
obstacles = []

# Setup fonksiyonu
def setup():
    # bireyler, hedef ve engeller'i global scope'tan al
    global entities, target, obstacles
    # 750x750'lik bir pencere oluştue
    size(750, 750)
    
    # Hedefi tanımla. Konum ve büyüklük ile.
    target = Target(PVector(100, 100), 20)
    # Engelleri tanımla. İstediğiniz kadar eklenebilir
    obstacles.append(Obstacle(PVector(200, 350), 100, 20))
    obstacles.append(Obstacle(PVector(450, 350), 100, 20))
    
    # Birey sayısınca, birey oluşturup, bireyler dizisine ekle
    for _ in range(NUMBER_OF_ENTITIES):
        entities.append(Entity())
    
# Draw fonksiyonu
def draw():
    # Frame, bireyler ve Jenerasyon değişkenlerini global scope'tan al
    global FRAME, entities, GENERATION
    # Arka alanı siyah yap
    background(0)
    
    # Tüm bireyleri tarayan bir döngü oluştur
    for entity in entities:
        # Bireyi göster
        entity.show()
        # Bireyi hareket ettir
        entity.move(FRAME % NUMBER_OF_GENES)
        # Birey ölmeli mi? Engele veya pencere kenarlarından birine çarptı mı?
        entity.die(obstacles)
        # Birey hedefe ulaştı mı?
        entity.success(target)
        
    # Engelleri çiz
    for obstacle in obstacles:
        obstacle.show()

    # Hedefi çiz
    target.show()
    
    # Bulunduğumuz Frame, toplam gen sayısına geldi mi?
    if FRAME == NUMBER_OF_GENES -1:
        # Gen havuzu oluştue
        gene_pool = []
        # Tümbireyleri tarayan bir döngü oluştur
        for entity in entities:
            # Bireyin skor'unu hesapla
            scr = entity.score(target)
            # Gen havuzuna, bireyin genini, skor sayısınca ekle
            for _ in range(scr):
                gene_pool.append(entity.dna)
            
        # Bireyler dizisini boşalt. Bireyleri öldür.
        entities = []
        # İhiyaç duyulan birey sayısınca bir döngü oluştur
        for _ in range(NUMBER_OF_ENTITIES):
            # Gen havuzundan rastgele iki gen seç
            parent1 = gene_pool[int(random(0, len(gene_pool) - 1))]
            parent2 = gene_pool[int(random(0, len(gene_pool) - 1))]
            
            # Bu iki geni kullanarak yeni bir birey oluştur
            new_antity = parent1.reproduce(parent2)
            # Bireyi bireyler dizisine ekle
            entities.append(new_antity)
            
        # Frame değerini sıfırla
        FRAME = 0
        # Jenerasyon değerini bir arttır
        GENERATION += 1
    
    # Jenerasyon değerini ekrana yaz
    stroke(255, 0, 0)
    textSize(35)
    text("GENRATION: {}".format(GENERATION), 40, 40)
    FRAME += 1


# Engel sınıfı
class Obstacle:
    # Constructor metod
    def __init__(self, pos, w, h):
        # Engelin konumu, genişliği ve yüksekliğini al
        self.pos = pos
        self.w = w
        self.h = h
        
    # Engeli göster
    def show(self):
        noStroke()
        fill(255, 0, 0)
        rect(self.pos.x, self.pos.y, self.w, self.h)


# Hedef sınıfı
class Target:
    # Constructor metod
    def __init__(self, pos, r):
        # Hedefin konumu ve yarıçapını al
        self.pos = pos
        self.r = r
        
    # Hedefi göster
    def show(self):
        noStroke()
        fill(0, 255, 0)
        circle(self.pos.x, self.pos.y, self.r * 2)


# DNA sınıfı
class DNA:
    # Constructor metod
    def __init__(self, gene=None):
        # Eğer gen verilmediyse, gen sayısınca gen oluştur. Rastgele hareketler
        self.gene = gene or [PVector(0, 0).random2D().setMag(STEP_MAG) for _ in range(NUMBER_OF_GENES)]
        
    # Üreme metodu
    def reproduce(self, other):
        # Bu bireyin ve diğer bireyin gen dizisinde rastgele bir nokta seç
        split_point = int(random(0, NUMBER_OF_GENES - 1))
        # Seçilen noktaya göre bu bireyin geinin sol tarafını
        # diğer bireyin gen listesinin sağ tarafıyla birleştir
        gene = self.gene[:split_point] + other.gene[split_point:]
        
        # Oluşan geni tarayan döngü
        for _ in range(len(gene)):
            # Eğer gelen verilen rastgele değer, mutasyon değerinden küçükse
            if random(1, 100) < MUTATION_RATE:
                # Seçilen gen bölgesini rastgele değiştir
                gene[int(random(0, NUMBER_OF_GENES - 1))] = PVector(0, 0).random2D().setMag(STEP_MAG)
        
        # Oluşan gen ile bir DNA ve bu DNA ile bir birey oluşturup, return et.
        return Entity(dna=DNA(gene=gene))


# Birey sınıfı
class Entity:
    # Constructor metod
    def __init__(self, pos=None, dna=None):
        # Bireyin pozisyonunu al. Verilmediyse x ekseninde orta y ekseninde aşağıda bir yeri seç
        self.pos = pos or PVector(width / 2, height - 50)
        # Bireyin dna'sını al. Verilmediyse rastgele bir tane oluştur. Rastgele hareket
        self.dna = dna or DNA()
        # Bireyin boyutu 5 olsun
        self.r = 5
        # Birey yaşıyor
        self.alive = True
        # Birey hedefe ulaşmış değil
        self.arrived = False
        # Bireyin kalan adım sayısı
        self.step_left = NUMBER_OF_GENES
        
    # Birey başarısı metodu
    def success(self, target):
        # Bireyin hedeften uaklığına bak
        d = dist(self.pos.x, self.pos.y, target.pos.x, target.pos.y)
        # Bireyin hedeften uzaklığı hedef be bireyin yarıçapından küçükse
        if d < self.r + target.r:
            # Birey hedefe ulaştı
            self.arrived = True
        else:
            # Değilse: Bireyin kalan adım sayısını bir azalt
            self.step_left -= 1
        
    # Bireyi göster
    def show(self):
        # Eğer birey yaşıyorsa
        if self.alive:
            noStroke()
            fill(255)
            circle(self.pos.x, self.pos.y, self.r * 2)
        
    # Bireyi hareket ettir
    def move(self, step):
        # Eğer birey yaşıyor ve hedefe ulaşmadıysa
        if self.alive and not self.arrived:
            self.pos.add(self.dna.gene[step])
        
    # Birey öldü mü metodu
    def die(self, obstacles):
        # Birey x ekseninde ekranın kenarına çarptı mı?
        if not self.r <= self.pos.x <= width - self.r:
            # Birey hayatta değil
            self.alive = False
        
        # Birey y ekseninde ekranın kenarına çarptı mı?
        if not self.r <= self.pos.y <= height - self.r:
            # Birey hayatta değil
            self.alive = False
            
        # Engeller dizisini tarayan döngü
        for obstacle in obstacles:
            # Birey bu engele çarptı mı?
            if obstacle.pos.x <= self.pos.x <= obstacle.pos.x + obstacle.w and obstacle.pos.y <= self.pos.y <= obstacle.pos.y + obstacle.h:
                # Birey hayatta değil
                self.alive = False
            
    # Skor hesaplama
    def score(self, target):
        # Birey hayatta değilse, skorunu sıfırlayan çarpan
        if self.alive:
            mult1 = 1
        else:
            mult1 = 0
        
        # Birey hedefe ulaşmış ise skorunu 100 katına çıkaran çarpan    
        if self.arrived:
            mult2 = 100
        else:
            mult2 = 1
            
        # Bireyin hedef ile arasındaki uzaklık
        d = dist(self.pos.x, self.pos.y, target.pos.x, target.pos.y)
        # Uzaklığı ters orantılı olarak 1 ile 200 arasına normalize et
        # Daha uzak daha az değer, daha yakın daha çok değer
        dist_score = map(d, 0, width, 200, 1)
        # skoru hesapla:
        # ölü ise 0 gelece.
        # Hedefe ulaştıysa 100 katına çıkacak
        # Uzaklığı az ise çok puan alacak
        # Kalan adımların 5 katı ise skoruna eklenecek
        my_score = int(mult1 * mult2 * (dist_score + self.step_left * 5))
        # Skor'u return et
        return my_score
        
