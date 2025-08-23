from django.contrib import admin
from .models import Jogador, Session, message, chat, Jogo, Jogo_daily, Jogo_custom, Jogo_VF
from .forms import JogadorForm, JogoForm, JogoDailyForm, JogoCustomForm, JogoVFForm

@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    form = JogadorForm
    list_display = ('id', 'name_public', 'name_user', 'name_email', 'last_login', 'status')
    search_fields = ('name_public', 'name_user', 'name_email')
    readonly_fields = ('id', 'last_login', 'status')
    list_filter = ('status', 'last_login')
    fieldsets = (
        (None, {
            'fields': ('name_public', 'name_user', 'name_email', 'name_password', 'last_login', 'status')
        }),
    )

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'public_key', 'get_root_player', 'status', 'data_inicio', 'data_termino', 'session_time')
    list_filter = ('status', 'data_inicio', 'data_termino')
    search_fields = ('public_key', 'root_player__name_user', 'root_player__name_public')

    def get_root_player(self, obj):
        return obj.root_player.name_user
    get_root_player.short_description = 'Root Player'


@admin.register(message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_sender', 'get_receivers', 'timestamp')
    search_fields = ('sender__name_user', 'receivers__name_user', 'texto')
    list_filter = ('timestamp',)

    def get_sender(self, obj):
        return obj.sender.name_user
    get_sender.short_description = 'Sender'

    def get_receivers(self, obj):
        return ", ".join([r.name_user for r in obj.receivers.all()])
    get_receivers.short_description = 'Receivers'

@admin.register(chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_participants', 'number_of_messages', 'frequency', 'created_at')
    search_fields = ('participants__name_user',)
    list_filter = ('created_at',)

    def get_participants(self, obj):
        return ", ".join([p.name_user for p in obj.participants.all()])
    get_participants.short_description = 'Participants'


@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    form = JogoForm
    list_display = ('id', 'session', 'data_inicio', 'data_fim')
    list_filter = ('session', 'data_inicio', 'data_fim')
    search_fields = ('id', 'session__id')
    filter_horizontal = ('players',)  # facilita escolha no ManyToMany


@admin.register(Jogo_daily)
class JogoDailyAdmin(admin.ModelAdmin):
    form = JogoDailyForm
    list_display = ('id', 'session', 'daily_date', 'data_inicio', 'data_fim')
    list_filter = ('daily_date', 'session')
    search_fields = ('id', 'session__id')
    filter_horizontal = ('players',)


@admin.register(Jogo_custom)
class JogoCustomAdmin(admin.ModelAdmin):
    form = JogoCustomForm
    list_display = ('id', 'session', 'data_inicio', 'data_fim')
    list_filter = ('session', 'data_inicio', 'data_fim')
    search_fields = ('id', 'session__id')
    filter_horizontal = ('players',)
    
@admin.register(Jogo_VF)
class JogoVFAdmin(admin.ModelAdmin):
    form = JogoVFForm
    list_display = ('id', 'session', 'pontuacao', 'acertos', 'data_inicio', 'data_fim')
    list_filter = ('session', 'data_inicio', 'data_fim', 'pontuacao', 'acertos')
    search_fields = ('id', 'session__id')
    filter_horizontal = ('players',)