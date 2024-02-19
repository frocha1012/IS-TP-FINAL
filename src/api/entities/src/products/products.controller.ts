import { Controller, Get, Post, Body, Param, Put, Delete } from '@nestjs/common';
import { ProductsService } from './products.service';

@Controller('products')
export class ProductsController {
    constructor(private readonly productService: ProductsService) {}

    @Get()
    async getAllProducts() {
        return this.productService.getAllProducts();
    }

    @Get(':id')
    async getProductById(@Param('id') id: string) {
        return this.productService.getProductById(id);
    }

    @Post()
    async createProduct(@Body() productData: { stock_code: string; description: string; unit_price: number }) {
        return this.productService.createProduct(productData);
    }

    @Put(':id')
    async updateProduct(@Param('id') id: string, @Body() productData: { stock_code?: string; description?: string; unit_price?: number }) {
        return this.productService.updateProduct(id, productData);
    }

    @Delete(':id')
    async deleteProduct(@Param('id') id: string) {
        return this.productService.deleteProduct(id);
    }
}
