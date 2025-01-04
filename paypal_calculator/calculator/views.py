from django.shortcuts import render
from django.http import JsonResponse
from decimal import Decimal, ROUND_HALF_UP


def calculate_fee(amount, direction='send'):
    """
    Calcula la comisión de PayPal basada en el monto y dirección
    Tarifa estándar: 5.4% + $0.30 USD
    """
    fee_rate = Decimal('0.054')
    fixed_fee = Decimal('0.30')

    if direction == 'send':
        fee = (amount * fee_rate + fixed_fee).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        net_amount = amount - fee
    else:  # receive
        # Para recibir X, necesitamos calcular cuánto debe enviar el remitente
        gross_amount = (amount + fixed_fee) / (Decimal('1') - fee_rate)
        gross_amount = gross_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        fee = gross_amount - amount

    return {
        'fee': fee,
        'gross_amount': amount if direction == 'send' else gross_amount,
        'net_amount': net_amount if direction == 'send' else amount
    }


def calculator_view(request):
    return render(request, 'calculator/calculator.html')


def calculate_api(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            direction = request.POST.get('direction', 'send')

            if amount <= 0:
                return JsonResponse({
                    'error': 'El monto debe ser mayor a 0'
                }, status=400)

            result = calculate_fee(amount, direction)

            return JsonResponse({
                'fee': str(result['fee']),
                'gross_amount': str(result['gross_amount']),
                'net_amount': str(result['net_amount'])
            })
        except (ValueError, decimal.InvalidOperation):
            return JsonResponse({
                'error': 'Monto inválido'
            }, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)