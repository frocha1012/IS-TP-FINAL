import { Controller, Get, Post, Body, Param, Delete, Put } from '@nestjs/common';
import { OrdersService } from './orders.service';

@Controller('orders')
export class OrdersController {
    constructor(private readonly ordersService: OrdersService) {}

    @Get()
    async getAllOrders() {
        return await this.ordersService.getAllOrders();
    }

    @Post()
    async createOrder(@Body() orderData: { invoice_no: string; invoice_date: Date; customer_id: number; country_ref: string }) {
        return this.ordersService.createOrder(orderData);
    }

    @Get(':id')
    async getOrderById(@Param('id') id: string) {
        return await this.ordersService.getOrderById(id);
    }

    @Put(':id')
    async updateOrder(@Param('id') id: string, @Body() orderData: { invoice_no?: string; invoice_date?: Date; customer_id?: number; country_ref?: string }) {
        return this.ordersService.updateOrder(id, orderData);
    }

    @Delete(':id')
    async deleteOrder(@Param('id') id: string) {
        return await this.ordersService.deleteOrder(id);
    }
}
