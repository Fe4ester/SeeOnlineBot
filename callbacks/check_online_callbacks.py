from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from states import CheckStates
from user_functions import database_functions as db

from datetime import datetime, timedelta

from keyboards import inline_keyboards as ikb
from keyboards import keyboards as rkb
import os
from aiogram.types import FSInputFile

from user_functions import graphical_functions as gf

router = Router()


async def get_monitored_users(callback, state, action_key, message_text, kb_generator, empty_message):
    monitored_users = await db.get_current_users(callback.from_user.id)
    if monitored_users:
        kb = await kb_generator(monitored_users)
        await callback.message.edit_text(message_text, reply_markup=kb)
        await state.update_data({action_key: monitored_users})
    else:
        await callback.message.edit_text(empty_message)
    await callback.answer()


@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    monitored_users = await db.get_current_users(callback.from_user.id)

    await state.clear()

    if monitored_users:
        user_list = '\n'.join([f"{idx + 1}. @{user[0]}" for idx, user in enumerate(monitored_users)])
        await callback.message.edit_text(f"Вы отслеживаете следующих пользователей:\n{user_list}", reply_markup=ikb.main_kb_1)
        await callback.answer()
    else:
        await callback.message.edit_text('Вы никого не отслеживаете, добавить?', reply_markup=ikb.main_kb_2)


@router.callback_query(F.data == 'add_user')
async def add_user_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Отправьте username пользователя', reply_markup=ikb.back_kb)
    await state.set_state(CheckStates.set)
    await callback.answer()


@router.callback_query(F.data == 'delete_user_menu')
async def delete_user_menu(callback: CallbackQuery, state: FSMContext):
    await get_monitored_users(
        callback,
        state,
        'monitored_users_delete',
        'Выберите пользователя, которого хотите удалить:',
        ikb.generate_delete_kb,
        'Нет пользователей для удаления'
    )


@router.callback_query(lambda call: call.data.startswith('delete_user:'))
async def delete_user(callback: CallbackQuery, state: FSMContext):
    username_to_delete = callback.data.split(':')[1]
    user_id = callback.from_user.id

    data = await state.get_data()
    monitored_users = [user for user in data.get('monitored_users_delete', []) if user[0] != username_to_delete]

    await db.delete_id(user_id, username_to_delete)
    await state.update_data(monitored_users_delete=monitored_users)

    if monitored_users:
        kb = await ikb.generate_delete_kb(monitored_users)
        await callback.message.edit_text(f'Пользователь @{username_to_delete} удален. Выберите следующего:',
                                         reply_markup=kb)
    else:
        await callback.message.edit_text('Все пользователи удалены')

    await callback.answer()


@router.callback_query(F.data == 'view_users_menu')
async def view_users_menu(callback: CallbackQuery, state: FSMContext):
    await get_monitored_users(
        callback,
        state,
        'monitored_users_view',
        'Выберите пользователя, которого хотите просмотреть:',
        ikb.generate_view_kb,
        'Нет пользователей для просмотра'
    )


@router.callback_query(lambda call: call.data.startswith('view_user:'))
async def view_user(callback: CallbackQuery):
    username = callback.data.split(':')[1]
    day_kb = await ikb.generate_day_kb(username)
    await callback.message.edit_text(f"Выберите период для пользователя @{username}:", reply_markup=day_kb)
    await callback.answer()


@router.callback_query(lambda call: call.data.startswith('view_day:'))
async def view_day(callback: CallbackQuery):
    _, username, day_choice = callback.data.split(':')

    days_map = {
        'today': (0, 'сегодня'),
        'yesterday': (1, 'вчера'),
        'day_before_yesterday': (2, 'позавчера')
    }

    delta_days, day_text = days_map[day_choice]
    selected_date = datetime.now().date() - timedelta(days=delta_days)

    periods_by_day = await db.get_online_periods(username)

    current_message_text = callback.message.text
    new_message_text = f"Нет данных по онлайну за {day_text}"

    if periods_by_day is False:
        if current_message_text != f"У пользователя @{username} закрыт онлайн":
            await callback.message.edit_text(f"У пользователя @{username} закрыт онлайн",
                                             reply_markup=ikb.back_kb)
    elif selected_date in periods_by_day:
        periods_for_day = {selected_date: periods_by_day[selected_date]}
        graph_path = await gf.create_activity_graph(periods_for_day, username, selected_date)

        try:
            photo = FSInputFile(graph_path)
            hide_kb = await ikb.generate_hide_kb(username)

            await callback.message.answer_photo(photo=photo, caption=f"График активности @{username} за {day_text}",
                                                reply_markup=hide_kb)

        finally:
            if os.path.exists(graph_path):
                os.remove(graph_path)
    else:
        if current_message_text != new_message_text:
            await callback.message.edit_text(new_message_text, reply_markup=await ikb.generate_day_kb(username))

    await callback.answer()


@router.callback_query(lambda call: call.data.startswith('hide_graph:'))
async def hide_graph(callback: CallbackQuery):
    await callback.message.delete()
